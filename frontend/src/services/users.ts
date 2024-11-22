import axiosInstance from "@/lib/axiosConfig";

// Define types for the API responses and requests
interface User {
  uuid: string;
  username: string;
  email: string;
  password: string;
  profile_photo: string;
  is_active: boolean;
  is_staff: boolean;
  is_superuser: boolean;
}

// User API calls
export const createUser = async (userData: Partial<User>) => {
  const response = await axiosInstance.post<User>("/users/", userData);
  return response.data;
};

export const updateUser = async (
  uuid: string,
  userData?: Partial<User>,
  formData?: FormData
) => {
  let response;
  if (formData) {
    response = await axiosInstance.put<User>(`/users/${uuid}/`, formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
  } else {
    response = await axiosInstance.put<User>(`/users/${uuid}/`, userData, {
      headers: {
        "Content-Type": "application/json",
      },
    });
  }
  return response.data;
};

export const deleteUser = async (uuid: string) => {
  const response = await axiosInstance.delete(`/users/${uuid}/`);
  return response.data;
};

export const verifyPassword = async (username: string, password: string) => {
  const response = await axiosInstance.post("/users/verify-password/", {
    username,
    password,
  });
  return response.data;
};

export const getUserByUUID = async (uuid: string) => {
  const response = await axiosInstance.get<User>(
    `/users/details-by-uuid/${uuid}/`
  );
  return response.data;
};

export const getUserByUsername = async (username: string) => {
  const response = await axiosInstance.get<User>(
    `/users/details-by-username/${username}/`
  );
  return response.data;
};

export const getUserByEmail = async (email: string) => {
  const response = await axiosInstance.get<User>(
    `/users/details-by-email/${email}/`
  );
  return response.data;
};
