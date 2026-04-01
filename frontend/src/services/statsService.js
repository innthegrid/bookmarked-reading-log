/* frontend/src/services/statsService.js */
import axios from "axios";
import { API_BASE } from "../config";

export const getStats = async (userId) => {
  const res = await axios.get(`${API_BASE}/stats`, {
    params: { user_id: userId }
  });
  return res.data;
};

export const getMonthlyStats = async (userId) => {
  const res = await axios.get(`${API_BASE}/stats/monthly`, {
    params: { user_id: userId }
  });
  return res.data;
};