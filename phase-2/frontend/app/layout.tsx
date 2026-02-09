import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import ErrorBoundary from "@/src/components/ErrorBoundary";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Todo App - Manage Your Tasks",
  description: "A modern, full-stack todo application built with Next.js and FastAPI. Create, manage, and track your tasks efficiently.",
  keywords: ["todo", "task management", "productivity", "next.js", "fastapi"],
  authors: [{ name: "Todo App Team" }],
  openGraph: {
    title: "Todo App - Manage Your Tasks",
    description: "A modern, full-stack todo application for efficient task management",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <ErrorBoundary>
          {children}
        </ErrorBoundary>
      </body>
    </html>
  );
}
