import axiosInstance from "@/lib/axiosConfig";

interface PlayerSettings {
  id: string;
  player: string;
  background_color: string;
  paddle_color: string;
}

export const createPlayerSettings = async (
  settingsData: Partial<PlayerSettings>
) => {
  const response = await axiosInstance.post<PlayerSettings>(
    "/player-settings/",
    settingsData
  );
  return response.data;
};

export const listPlayerSettings = async () => {
  const response = await axiosInstance.get<PlayerSettings[]>(
    "/player-settings/"
  );
  return response.data;
};

export const getPlayerSettingsByPlayer = async (uuid: string) => {
  const response = await axiosInstance.get<PlayerSettings[]>(
    `/player-settings/by-player/${uuid}/`
  );
  return response.data;
};
