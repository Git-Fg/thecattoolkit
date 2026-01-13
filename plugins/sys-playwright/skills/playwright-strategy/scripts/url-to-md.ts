import { spawn } from "child_process";
import * as path from "path";

/**
 * Advanced wrapper for @just-every/crawl via npx.
 * Optimized for LLM consumption with token awareness and robust error handling.
 * Supports multiple URLs in a single execution.
 */

interface CrawlResult {
  url: string;
  markdown: string;
  title?: string;
  links?: string[];
  error?: string;
  metadata?: {
    length: number;
    truncated: boolean;
    duration: number;
  };
}

interface Options {
  pages?: number;
  concurrency?: number;
  respectRobots?: boolean;
  sameOriginOnly?: boolean;
  userAgent?: string;
  cacheDir?: string;
  timeout?: number;
  maxContentLength?: number;
  parallel?: boolean; // Run multiple URLs in parallel
}

async function runCrawl(url: string, options: Options = {}): Promise<CrawlResult[]> {
  const startTime = Date.now();
  return new Promise((resolve, reject) => {
    const args = ["@just-every/crawl", url, "--output", "json"];
    
    if (options.pages) args.push("--pages", options.pages.toString());
    if (options.concurrency) args.push("--concurrency", options.concurrency.toString());
    if (options.respectRobots === false) args.push("--no-robots");
    if (options.sameOriginOnly === false) args.push("--all-origins");
    if (options.userAgent) args.push("--user-agent", options.userAgent);
    if (options.timeout) args.push("--timeout", options.timeout.toString());
    if (options.cacheDir) args.push("--cache-dir", options.cacheDir);

    const child = spawn("npx", args);

    let stdout = "";
    let stderr = "";

    child.stdout.on("data", (data) => {
      stdout += data.toString();
    });

    child.stderr.on("data", (data) => {
      stderr += data.toString();
    });

    child.on("close", (code) => {
      const duration = Date.now() - startTime;
      
      if (code !== 0 && code !== null) {
        // We resolve with an error object instead of rejecting for batch processing
        resolve([{
            url,
            markdown: "",
            error: `Failed with code ${code}: ${stderr}`,
            metadata: { length: 0, truncated: false, duration }
        }]);
        return;
      }

      try {
        const jsonStart = stdout.indexOf("[");
        const objStart = stdout.indexOf("{");
        
        let start = -1;
        if (jsonStart !== -1 && (objStart === -1 || jsonStart < objStart)) start = jsonStart;
        else if (objStart !== -1) start = objStart;

        if (start === -1) {
            resolve([{
                url,
                markdown: "",
                error: "No JSON found in output. Blocked or empty result.",
                metadata: { length: 0, truncated: false, duration }
            }]);
            return;
        }

        const data = JSON.parse(stdout.substring(start));
        const rawResults: any[] = Array.isArray(data) ? data : [data];

        const results: CrawlResult[] = rawResults.map((res: any) => {
          let markdown = res.markdown || "";
          let truncated = false;
          const originalLength = markdown.length;

          if (options.maxContentLength && markdown.length > options.maxContentLength) {
            markdown = markdown.substring(0, options.maxContentLength) + "\n\n... [TRUNCATED FOR LLM OPTIMIZATION] ...";
            truncated = true;
          }

          return {
            url: res.url,
            markdown,
            title: res.title,
            links: res.links,
            error: res.error,
            metadata: {
              length: originalLength,
              truncated,
              duration
            }
          };
        });

        resolve(results);
      } catch (e) {
        resolve([{
            url,
            markdown: "",
            error: `Failed to parse output: ${e}`,
            metadata: { length: 0, truncated: false, duration }
        }]);
      }
    });
  });
}

// Parse CLI arguments
const args = process.argv.slice(2);
const urls = args.filter(a => a.startsWith("http"));

if (urls.length === 0) {
  console.error(JSON.stringify({ 
    status: "error", 
    message: "Missing URL(s)",
    usage: "bun run url-to-md.ts <url1> [url2] ... [options]",
    options: [
      "--pages <n>",
      "--concurrency <n>",
      "--no-robots",
      "--all-origins",
      "--user-agent <string>",
      "--timeout <ms>",
      "--cache-dir <path>",
      "--max-length <n>",
      "--parallel"
    ]
  }));
  process.exit(1);
}

function getArg(flag: string): string | undefined {
  const idx = args.indexOf(flag);
  return idx !== -1 && args[idx + 1] ? args[idx + 1] : undefined;
}

const options: Options = {
  pages: parseInt(getArg("--pages") || "1"),
  concurrency: parseInt(getArg("--concurrency") || "3"),
  respectRobots: !args.includes("--no-robots"),
  sameOriginOnly: !args.includes("--all-origins"),
  userAgent: getArg("--user-agent"),
  timeout: parseInt(getArg("--timeout") || "30000"),
  cacheDir: getArg("--cache-dir") || ".cache",
  maxContentLength: parseInt(getArg("--max-length") || "30000"),
  parallel: args.includes("--parallel")
};

async function main() {
    let allResults: CrawlResult[] = [];
    
    if (options.parallel) {
        const promises = urls.map(url => runCrawl(url, options));
        const resultsArray = await Promise.all(promises);
        allResults = resultsArray.flat();
    } else {
        for (const url of urls) {
            const results = await runCrawl(url, options);
            allResults.push(...results);
        }
    }

    const hasErrors = allResults.some(r => r.error);
    const allEmpty = allResults.every(r => !r.markdown || r.markdown.trim().length < 50);
    
    const output: any = { 
      status: "success", 
      urlCount: urls.length,
      resultCount: allResults.length,
      results: allResults 
    };

    if (allEmpty && allResults.length > 0) {
      output.recommendation = "Content seems empty or blocked for most URLs. Consider full Playwright mode.";
    }

    console.log(JSON.stringify(output, null, 2));
}

main().catch(error => {
    console.error(JSON.stringify({ status: "error", message: error.message }));
    process.exit(1);
});
