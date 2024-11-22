import axiosInstance from "@/lib/axiosConfig";

interface Game {
  id: string;
  player1: string;
  player2: string;
  score1: number;
  score2: number;
  is_tournament: boolean;
}

export const createGame = async (gameData: Partial<Game>) => {
  const response = await axiosInstance.post<Game>("/games/", gameData);
  return response.data;
};

export const getAllGamesByPlayer = async (uuid: string) => {
  const response = await axiosInstance.get<Game[]>(
    `/games/all-by-player/${uuid}/`
  );
  return response.data;
};
