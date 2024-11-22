"use client";

import SignInOutButton from "@/components/login-button";
import { getSession } from "next-auth/react";
import { useEffect } from "react";

export default function Home() {
  useEffect(() => {
    getSession()
      .then((session) => {
        console.log("session in home");
        console.dir(session, { depth: 5 });
      })
      .catch(console.error);
  }, []);

  return (
    <div>
      <SignInOutButton />
    </div>
  );
}
