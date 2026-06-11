/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import express from "express";
import path from "path";
import { createServer as createViteServer } from "vite";
import { generateStaticHtml, SiteContent } from "./src/utils/staticGenerator";

async function startServer() {
  const app = express();
  const PORT = 3000;

  // Body parsing of JSON for state synchronization
  app.use(express.json({ limit: "20mb" }));
  app.use(express.urlencoded({ limit: "20mb", extended: true }));

  // API endpoint to compile full standalone HTML
  app.post("/api/compile-html", (req, res) => {
    try {
      const content = req.body as SiteContent;
      if (!content || !content.hero || !content.seoTool) {
        return res.status(400).json({ error: "Invalid SiteContent structure" });
      }
      
      const html = generateStaticHtml(content);
      res.json({ success: true, html });
    } catch (e: any) {
      res.status(500).json({ error: e.message || "Failed to compile static template HTML" });
    }
  });

  // Serve Vite app in development vs static SPA in production
  if (process.env.NODE_ENV !== "production") {
    console.log("Starting full-stack server in Development Mode (with Vite HMR enabled)...");
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: "spa",
    });
    app.use(vite.middlewares);
  } else {
    console.log("Starting full-stack server in Production Mode...");
    const distPath = path.join(process.cwd(), "dist");
    app.use(express.static(distPath));
    app.get("*", (req, res) => {
      res.sendFile(path.join(distPath, "index.html"));
    });
  }

  app.listen(PORT, "0.0.0.0", () => {
    console.log(`ASM Digital Solutions Server successfully established on port ${PORT}`);
  });
}

startServer().catch((err) => {
  console.error("FATAL: Failed to initialize full-stack ecosystem", err);
  process.exit(1);
});
