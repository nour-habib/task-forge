/**
 * Download utilities for images and code.
 */

export function downloadImage(assetUrl: string, filename: string) {
  const safeName = filename.replace(/\s+/g, "-").toLowerCase();
  const finalName = `task-forge-${safeName}.png`;

  if (assetUrl.startsWith("data:")) {
    fetch(assetUrl)
      .then((r) => r.blob())
      .then((blob) => {
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = finalName;
        a.click();
        URL.revokeObjectURL(url);
      });
  } else {
    const a = document.createElement("a");
    a.href = assetUrl;
    a.download = finalName;
    a.target = "_blank";
    a.rel = "noopener noreferrer";
    a.click();
  }
}

export function downloadCode(code: string, agentName: string) {
  const safeName = agentName.replace(/\s+/g, "-").toLowerCase();
  const blob = new Blob([code], { type: "text/html" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `task-forge-${safeName}.html`;
  a.click();
  URL.revokeObjectURL(url);
}
