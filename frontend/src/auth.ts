import { AuthOptions, getServerSession } from "next-auth";
// import FortyTwoProvider from "next-auth/providers/42-school";
import CredentialsProvider from "next-auth/providers/credentials";

const backendUrl = process.env.BACKEND_URL;

const authOptions: AuthOptions = {
  providers: [
    // FortyTwoProvider({
    //   clientId: process.env.FORTY_TWO_CLIENT_ID as string,
    //   clientSecret: process.env.FORTY_TWO_CLIENT_SECRET as string,
    // }),
    CredentialsProvider({
      id: "credentials",
      name: "Credentials",
      credentials: {
        email: {
          label: "Email Address",
          type: "email",
          placeholder: "Enter email address",
        },
        password: {
          label: "Password",
          type: "password",
          placeholder: "Enter password",
        },
      },
      // TODO: Rewrite this API call to use the validation endpoint of the backend
      async authorize(credentials) {
        const res = await fetch(`${backendUrl}/users/verify-password/`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            username: credentials?.email,
            password: credentials?.password,
          }),
        });
        const user = await res.json();
        if (res.ok && user) {
          console.log("authorize user is ");
          console.dir(user, { depth: 5 });
          return user;
        }
        return null;
      },
    }),
  ],
  secret: process.env.NEXTAUTH_SECRET,
  session: {
    strategy: "jwt", // Use JWT for session management
  },
  callbacks: {
    async jwt({ token, account, profile }) {
      // Attach additional data to the token during sign-in
      // console.log("jwt token ", token);
      // console.dir(token, { depth: 5 });
      // console.log("jwt account ", account);
      // console.dir(account, { depth: 5 });
      // console.log("jwt profile ");
      // console.dir(profile, { depth: 5 });
      if (account && profile) {
        token.id = profile.id;
        token.name = profile.name;
        token.email = profile.email;
      }
      return token;
    },
    async session({ session, token }) {
      // console.log("session in auth is ");
      // console.dir(session, { depth: 5 });
      // console.log("session token ");
      // console.dir(token, { depth: 5 });
      const newSession = { ...session, user: { ...session.user } };
      // Expose token details to the session
      if (!newSession.user) {
        newSession.user = {
          id: 0,
          name: "",
          email: "",
        };
      }
      if (newSession.user) {
        newSession.user.id = token.id;
        newSession.user.name = token.name;
        newSession.user.email = token.email;
      }
      return newSession;
    },
  },
};

const getServerSideSession = () => getServerSession(authOptions);

export { authOptions, getServerSideSession };
