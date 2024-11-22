"use client";

import { useSession } from "next-auth/react";
import { useState, useEffect } from "react";
import { getUserByEmail, updateUser } from "@/services/users";

export default function Me() {
  const [username, setUsername] = useState<string>("");
  const [password, setPassword] = useState("");
  const [profilePhoto, setProfilePhoto] = useState<File | null>(null);
  const [message, setMessage] = useState("");
  const [userUUID, setUserUUID] = useState<string>("");
  const session = useSession();

  useEffect(() => {
    console.log("session is ", session);
    async function fetchSession() {
      if (session) {
        const email = session.data?.user?.email;
        if (email) {
          const userData = await getUserByEmail(email);
          console.log("user Data is ", userData);
          setUserUUID(userData.uuid);
        }
      }
    }
    fetchSession();
  }, [session]);

  const handleUsernameChange = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    try {
      await updateUser(userUUID, { username });
      setMessage("Username updated successfully");
    } catch (error) {
      console.log("error is ", error);
      setMessage("Failed to update username");
    }
  };

  const handlePasswordChange = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    try {
      await updateUser(userUUID, { password });
      setMessage("Password updated successfully");
    } catch (error) {
      console.log("error is ", error);
      setMessage("Failed to update password");
    }
  };

  const handleProfilePhotoChange = async (
    e: React.FormEvent<HTMLFormElement>
  ) => {
    e.preventDefault();
    if (profilePhoto) {
      const formData = new FormData();
      formData.append("profile_photo", profilePhoto);
      try {
        await updateUser(userUUID, undefined, formData);
        setMessage("Profile photo updated successfully");
      } catch (error) {
        console.log("error is ", error);
        setMessage("Failed to update profile photo");
      }
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="bg-white p-8 rounded shadow-md w-full max-w-md">
        <h2 className="text-2xl font-bold mb-6 text-center text-black">
          Update Profile
        </h2>
        {message && <p className="mb-4 text-center text-black">{message}</p>}
        <form onSubmit={handleUsernameChange} className="mb-4">
          <div className="mb-4">
            <label className="block text-gray-700 text-black">Username:</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
              className="w-full px-3 py-2 border rounded"
            />
          </div>
          <button
            type="submit"
            className="w-full bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600"
          >
            Update Username
          </button>
        </form>
        <form onSubmit={handlePasswordChange} className="mb-4">
          <div className="mb-4">
            <label className="block text-gray-700 text-black">Password:</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full px-3 py-2 border rounded"
            />
          </div>
          <button
            type="submit"
            className="w-full bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600"
          >
            Update Password
          </button>
        </form>
        <form onSubmit={handleProfilePhotoChange}>
          <div className="mb-4">
            <label className="block text-gray-700 text-black">
              Profile Photo:
            </label>
            <input
              type="file"
              onChange={(e) => {
                if (e.target.files) {
                  setProfilePhoto(e.target.files[0]);
                }
              }}
              required
              className="w-full px-3 py-2 border rounded"
            />
          </div>
          <button
            type="submit"
            className="w-full bg-blue-500 text-white py-2 px-4 rounded hover:bg-blue-600"
          >
            Update Profile Photo
          </button>
        </form>
      </div>
    </div>
  );
}
