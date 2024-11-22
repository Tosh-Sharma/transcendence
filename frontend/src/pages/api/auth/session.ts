import { NextApiRequest, NextApiResponse } from "next";
import axios from "axios";
import { getSession } from "next-auth/react";

export default async function session(
  req: NextApiRequest,
  res: NextApiResponse
) {
  try {
    // Get the session from next-auth
    const session = await getSession({ req });

    console.log("session in session file is ");
    console.dir(session, { depth: 5 });

    // If there is no session, return a 401 Unauthorized response
    if (!session) {
      return res.status(401).json({ message: "Unauthorized" });
    }

    // Proxy the request to your backend endpoint
    const response = await axios.get(
      `${process.env.BACKEND_URL}/users/detail-by-email/${session.user?.email}/`,
      {
        // headers: {
        //   Authorization: `Bearer ${session.accessToken}`, // Use the access token from the session
        // },
      }
    );

    // Return the response from the backend
    return res.status(response.status).json(response.data);
  } catch (error) {
    console.error("Error fetching session:", error);
    return res.status(500).json({ message: "Internal Server Error" });
  }
}
