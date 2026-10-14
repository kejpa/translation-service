<template>
  <div class="about">
    <h1>About Translation Service</h1>

    <p>
      Translation Service is a self-hosted Translation Memory system for
      DOCX documents with integrated AI-assisted translation.
    </p>

    <h2>Workflow</h2>

    <ol>
      <li>Import Finnish and Swedish document pairs.</li>
      <li>Build and maintain a Translation Memory.</li>
      <li>Translate DOCX documents using Translation Memory matches.</li>
      <li>Use Ollama when no suitable match exists.</li>
      <li>Download translated documents.</li>
    </ol>

    <h2>Features</h2>

    <ul>
      <li>Translation Memory management</li>
      <li>DOCX import and translation</li>
      <li>Exact and fuzzy matching</li>
      <li>Translation statistics</li>
      <li>Local AI translation using Ollama</li>
      <li>Dashboard monitoring</li>
    </ul>

    <h2>Technology</h2>

    <ul>
      <li>Vue 3</li>
      <li>FastAPI</li>
      <li>SQLite</li>
      <li>Ollama</li>
      <li>Docker</li>
    </ul>

    <h2>First-Time Setup</h2>

    <ol>
      <li>Verify that the database is connected.</li>
      <li>Verify that Ollama is connected.</li>
      <li>
        If the configured model is not installed, use the Dashboard to install it.
      </li>
      <li>Import translation memory documents.</li>
      <li>Start translating.</li>
    </ol>
  </div>
</template>
