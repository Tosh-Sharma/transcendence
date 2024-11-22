"use client";
import { signIn, signOut, useSession } from "next-auth/react";

function SignIn() {
  const { data: session } = useSession();

  console.log("session in Login Button", session);

  if (session) {
    return (
      <div>
        <h1>Welcome, {session?.user?.name}!</h1>
        <p>Email: {session?.user?.email}</p>
        <button onClick={() => signOut()}>Sign out</button>
      </div>
    );
  }

  return (
    <div>
      {/* <h1>Sign In</h1> */}
      <button onClick={() => signIn("42")}>Sign in with 42</button>
    </div>
  );
}

export default SignIn;
