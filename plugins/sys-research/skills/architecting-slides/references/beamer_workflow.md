# LaTeX Beamer Workflow Guide

Create professional presentations with mathematical content using LaTeX Beamer.

## Why Beamer?

**Advantages**:
- Beautiful mathematics and equations
- Consistent, professional appearance
- Version control friendly (plain text)
- Excellent for algorithms and code
- Reproducible and programmatic

**Best for**: Mathematical content, consistent formatting, version control, technical presentations

## Templates Available

Pre-built templates for different talk types:

- **`assets/beamer_template_conference.tex`**: 15-minute conference talk
- **`assets/beamer_template_seminar.tex`**: 45-minute academic seminar
- **`assets/beamer_template_defense.tex`**: Dissertation defense

## Step-by-Step Process

### Step 1: Choose Template

Select the appropriate template based on your presentation duration and type.

### Step 2: Customize Theme and Colors

Beamer comes with built-in themes. Common themes include:

**Dark Themes**:
- `Madrid` (dark blue, professional)
- `Singapore` (dark gray, clean)
- `CambridgeUS` (dark red, academic)

**Light Themes**:
- `Antibes` (white, colorful)
- `Copenhagen` (white, blue accents)
- `Berkeley` (white, green accents)

**Customization Example**:
```latex
% In preamble
 usetheme{Madrid}
 \usecolortheme{beaver}
 \usefonttheme{structurebold}
 \setbeamercolor{title}{fg=darkblue}
 \setbeamercolor{author}{fg=gray}
```

### Step 3: Add Content

LaTeX native support for:
- **Equations**: Use `equation`, `align`, `gather` environments
- **Code**: Use `lstlisting` or `verbatim` environments
- **Algorithms**: Use `algorithm` and `algorithmic` packages
- **Figures**: Use `includegraphics` with proper sizing
- **Tables**: Use standard LaTeX table environments

### Step 4: Compile to PDF

```bash
# Compile with pdflatex
pdflatex presentation.tex
pdflatex presentation.tex  # Run twice for proper references
```

### Step 5: Convert to Images (Optional)

For visual validation:
```bash
# Using the pdf_to_images script
python scripts/pdf_to_images.py presentation.pdf review/slides --dpi 150
```

## Example Presentation Structure

```latex
\documentclass{beamer}

% Packages
\usepackage{graphicx}
\usepackage{amsmath, amssymb}
\usepackage{listings}

% Theme
\usetheme{Madrid}
\usecolortheme{beaver}

% Title Page
\title{Your Presentation Title}
\subtitle{Subtitle if needed}
\author{Your Name}
\institute{Your Institution}
\date{\today}

\begin{document}

\begin{frame}
  \titlepage
\end{frame}

\begin{frame}{Overview}
  \tableofcontents
\end{frame}

\section{Introduction}
\begin{frame}{Background}
  \begin{itemize}
    \item Point 1
    \item Point 2
  \end{itemize}
\end{frame}

\section{Methods}
\begin{frame}{Algorithm}
  \begin{algorithmic}
    \State Initialize parameters
    \State Perform computation
    \State Return result
  \end{algorithmic}
\end{frame}

\section{Results}
\begin{frame}{Key Findings}
  \begin{figure}
    \includegraphics[width=0.8\textwidth]{figure.png}
    \caption{Your Figure Caption}
  \end{figure}
\end{frame}

\section{Conclusion}
\begin{frame}{Summary}
  \begin{itemize}
    \item Main point 1
    \item Main point 2
  \end{itemize}
\end{frame}

\end{document}
```

## Mathematics in Beamer

Beamer excels at mathematical presentations.

### Equations
```latex
\begin{frame}{Mathematical Model}

The key equation is:
\begin{equation}
  f(x) = \sum_{i=1}^{n} a_i x^i
\end{equation}

\end{frame}
```

### Multi-line Equations
```latex
\begin{frame}{Derivation}

\begin{align}
  \frac{\partial L}{\partial \theta} &= \frac{\partial}{\partial \theta} \sum_{i=1}^{n} \log p(x_i | \theta) \\
  &= \sum_{i=1}^{n} \frac{\partial}{\partial \theta} \log p(x_i | \theta)
\end{align}

\end{frame}
```

### Theorems and Definitions
```latex
\newtheorem{theorem}{Theorem}[section]
\newtheorem{definition}{Definition}[section]

\begin{frame}{Key Theorem}

\begin{theorem}
If conditions A and B hold, then result C follows.
\end{theorem}

\begin{proof}
The proof follows from...
\end{proof}

\end{frame}
```

## Code Listings

### Syntax Highlighting
```latex
\lstset{
  language=Python,
  basicstyle=\ttfamily,
  keywordstyle=\color{blue},
  stringstyle=\color{red},
  commentstyle=\color{green}
}

\begin{frame}{Algorithm}

\lstinputlisting[language=Python]{code.py}

\end{frame}
```

### Inline Code
```latex
\begin{frame}{Implementation}

The function \texttt{train\_model()} performs:

\begin{enumerate}
  \item Load data
  \item Initialize weights
  \item Train for epochs
\end{enumerate}

\end{frame}
```

## Figures and Tables

### Including Figures
```latex
\begin{frame}{Results}

\begin{figure}
  \centering
  \includegraphics[width=0.7\textwidth]{experiment_results.png}
  \caption{Experimental Results}
  \label{fig:results}
\end{figure}

\end{frame}
```

### Tables
```latex
\begin{frame}{Comparison}

\begin{table}
  \caption{Model Performance}
  \begin{tabular}{|l|c|c|}
    \hline
    Model & Accuracy & F1-Score \\
    \hline
    Baseline & 0.85 & 0.82 \\
    Proposed & 0.92 & 0.89 \\
    \hline
  \end{tabular}
\end{table}

\end{frame}
```

## Animations and Overlays

Beamer supports sophisticated animations:

### Itemize Animation
```latex
\begin{frame}{Progressive Disclosure}

\begin{itemize}
  \item<1-> Point 1 (appears on slide 1)
  \item<2-> Point 2 (appears on slide 2)
  \item<3-> Point 3 (appears on slide 3)
\end{itemize}

\end{frame}
```

### Reveal Equations
```latex
\begin{frame}{Derivation}

\begin{align}
  f(x) &= x^2 + 2x + 1 \\
  \uncover<2->{&= (x+1)^2} \\
  \uncover<3->{&= \text{perfect square}}
\end{align}

\end{frame}
```

## Themes and Customization

### Theme Combinations

Popular combinations:
- `Madrid` + `beaver` (dark blue, professional)
- `Singapore` + `whale` (dark gray, clean)
- `Copenhagen` + `seahorse` (light, colorful)
- `Berkeley` + `albatross` (light, green accents)

### Custom Colors
```latex
\setbeamercolor{title}{fg=darkblue}
\setbeamercolor{author}{fg=gray}
\setbeamercolor{institute}{fg=lightgray}
\setbeamercolor{date}{fg=lightgray}
```

### Custom Font Sizes
```latex
\setbeamerfont{title}{size=\Large}
\setbeamerfont{author}{size=\normalsize}
\setbeamerfont{institute}{size=\small}
```

## Tips and Best Practices

1. **Compile Twice**: LaTeX needs two passes for proper cross-references
2. **Use `\pause`**: For simple progressive disclosure
3. **Limit Text**: Keep slides minimal, let equations shine
4. **Consistent Spacing**: Use `\vfill` to distribute content vertically
5. **Reference Labels**: Use `\label{}` and `\ref{}` for navigation
6. **Backup Slides**: Use `\appendix` for backup material

## Troubleshooting

### Compilation Issues
- **Missing packages**: Add `\usepackage{package_name}` to preamble
- **Font errors**: Use `\usepackage[T1]{fontenc}` for better font support
- **Figure not found**: Check file path and extensions

### Layout Issues
- **Text too small**: Increase `\documentclass[14pt]{beamer}` point size
- **Figures too large**: Use `\includegraphics[width=0.8\textwidth]{file}`
- **Page breaks**: Use `\newpage` or `\clearpage`

## References

For complete LaTeX Beamer documentation, see:
- `references/beamer_guide.md`: Comprehensive guide with all features
- See `assets/` for ready-to-use templates (e.g., `beamer_template_conference.tex`)
- LaTeX Beamer User Guide: Official documentation

## Quick Start

1. Choose template: `assets/beamer_template_conference.tex`
2. Customize theme: `\usetheme{Madrid}`
3. Add content: equations, algorithms, figures
4. Compile: `pdflatex presentation.tex`
5. Review and iterate

Beamer is ideal for technical presentations requiring precise mathematical formatting.
