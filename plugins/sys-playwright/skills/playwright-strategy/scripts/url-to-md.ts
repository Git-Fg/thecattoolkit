import { spawn } from "child_process";
import * as path from "path";

/**
 * Wraps @just-every/crawl via npx to provide fast URL-to-Markdown conversion.
 * Returns structured JSON for the Agent to consume.
 */

interface CrawlResult {
  url: string;
  markdown: string;
  title?: string;
  links?: string[];
  error?: string;
}

async function runCrawl(url: string, options: { pages?: number; concurrency?: number } = {}): Promise<CrawlResult[]> {
  return new Promise((resolve, reject) => {
    const args = ["@just-every/crawl", url, "--output", "json"];
    
    if (options.pages) {
      args.push("--pages", options.pages.toString());
    }
    if (options.concurrency) {
      args.push("--concurrency", options.concurrency.toString());
    }

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
      if (code !== 0) {
        reject(new Error(`npx @just-every/crawl failed with code ${code}: ${stderr}`));
        return;
      }

      try {
        // The library might output logs before the JSON, so we find the first '[' or '{'
        const jsonStart = stdout.indexOf("[");
        if (jsonStart === -1) {
            // Try object if array not found
            const objStart = stdout.indexOf("{");
            if (objStart === -1) {
                throw new Error("No JSON found in output");
            }
            const data = JSON.parse(stdout.substring(objStart));
            resolve(Array.isArray(data) ? data : [data]);
            return;
        }
        const data = JSON.parse(stdout.substring(jsonStart));
        resolve(Array.isArray(data) ? data : [data]);
      } catch (e) {
        reject(new Error(`Failed to parse JSON output: ${e}\nRaw output: ${stdout}`));
      }
    });
  });
}

const url = process.argv[2];
const pages = process.argv[3] ? parseInt(process.argv[3], 10) : 1;
const concurrency = process.argv[4] ? parseInt(process.argv[4], 10) : 3;

if (!url) {
  console.error(JSON.stringify({ status: "error", message: "Usage: bun run url-to-md.ts <url> [pages] [concurrency]" }));
  process.exit(1);
}

runCrawl(url, { pages, concurrency })
  .then((results) => {
    console.log(JSON.stringify({ status: "success", results }, null, 2));
  })
  .catch((error) => {
    console.error(JSON.stringify({ status: "error", message: error.message }));
    process.exit(1);
  });
