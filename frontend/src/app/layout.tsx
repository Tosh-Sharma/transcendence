import React from "react";
import type { Metadata } from "next";
import localFont from "next/font/local";

import Navbar from "@/components/navbar";
import { getServerSideSession } from "@/auth";

import Providers from "@/app/providers";
import "./globals.css";

const geistSans = localFont({
  src: "./fonts/GeistVF.woff",
  variable: "--font-geist-sans",
  weight: "100 900",
});
const geistMono = localFont({
  src: "./fonts/GeistMonoVF.woff",
  variable: "--font-geist-mono",
  weight: "100 900",
});

export const metadata: Metadata = {
  title: "The Pong Game",
  description: "Created by Tosh Sharma",
};

export default async function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const session = await getServerSideSession();

  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <Providers session={session}>
          <Navbar />
          {children}
        </Providers>
      </body>
    </html>
  );
}

/**
Client side component that can work with sessions
// in components/client-component.tsx

"use client"

import { useSession } from "next-auth/react"

export default function MyClientComponent() {

    const { data: session, status } = useSession()

    // do what you need to with the session and the auth status...

    return (
        // some jsx...
    )
}
*/

/**
 * Server side component that can work with sessions as follows:
// in components/server-component.tsx

import { getServerSideSession } from "@/auth"

export default function MyServerComponent() {
    const session = await getServerSideSession()

    // do whatever you need to with the session...
    return (
        // some jsx...
    )
}
 */
