import type { AppProps } from "next/app";
import Head from "next/head";
import { useEffect } from "react";
import "../styles/globals.css";

export default function App({ Component, pageProps }: AppProps) {
  useEffect(() => {
    if ("serviceWorker" in navigator) {
      window.addEventListener("load", () => {
        navigator.serviceWorker.register("/sw.js").then(
          (registration) => {
            console.log(
              "Service Worker registration successful:",
              registration.scope,
            );
          },
          (err) => {
            console.log("Service Worker registration failed:", err);
          },
        );
      });
    }
  }, []);

  return (
    <>
      <Head>
        <meta charSet="utf-8" />
        <meta httpEquiv="X-UA-Compatible" content="IE=edge" />
        <meta
          name="viewport"
          content="width=device-width,initial-scale=1,minimum-scale=1,maximum-scale=5,user-scalable=yes"
        />
        <meta
          name="description"
          content="Revolutionary distributed AGI system with exponential intelligence growth"
        />
        <meta
          name="keywords"
          content="AI, AGI, artificial intelligence, consciousness, think ai"
        />
        <title>Think AI - Distributed AGI System</title>

        <link rel="manifest" href="/manifest.json" />
        <link
          href="/icons/icon-16x16.png"
          rel="icon"
          type="image/png"
          sizes="16x16"
        />
        <link
          href="/icons/icon-32x32.png"
          rel="icon"
          type="image/png"
          sizes="32x32"
        />
        <link rel="apple-touch-icon" href="/icons/icon-192x192.png" />
        <meta name="theme-color" content="#000000" />

        <meta name="mobile-web-app-capable" content="yes" />
        <meta name="apple-mobile-web-app-capable" content="yes" />
        <meta
          name="apple-mobile-web-app-status-bar-style"
          content="black-translucent"
        />
        <meta name="apple-mobile-web-app-title" content="Think AI" />

        <meta property="og:type" content="website" />
        <meta property="og:title" content="Think AI - Distributed AGI System" />
        <meta
          property="og:description"
          content="Revolutionary distributed AGI system with exponential intelligence growth"
        />
        <meta property="og:site_name" content="Think AI" />
        <meta property="og:url" content="https://think-ai.vercel.app" />
        <meta property="og:image" content="/icons/icon-512x512.png" />
      </Head>
      <Component {...pageProps} />
    </>
  );
}
