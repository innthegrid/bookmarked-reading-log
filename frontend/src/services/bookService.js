/* frontend/src/services/bookService.js */
import axios from "axios";
import { API_BASE } from "../config";

const api = axios.create({
  baseURL: API_BASE,
  headers: {
    "Content-Type": "application/json"
  }
});

export const getLibrary = async (userId) => {
  if (!userId) return [];
  try {
    const res = await api.get("/library", {
      params: { user_id: userId }
    });
    return res.data;
  } catch (err) {
    console.error("Failed to fetch library", err);
    return [];
  }
};

export const addBook = async (data) => {
  try {
    const res = await api.post("/library/add", data);
    return res.data;
  } catch (err) {
    console.error("Failed to add book", err);
    throw err;
  }
};

export const updateBook = async (userBookId, data) => {
  if (!userBookId) return;
  try {
    const res = await api.patch(`/library/${userBookId}`, data);
    return res.data;
  } catch (err) {
    console.error("Failed to update book", err);
    throw err;
  }
};

export const deleteBook = async (userBookId) => {
  if (!userBookId) return;
  try {
    const res = await api.delete(`/library/${userBookId}`);
    return res.data;
  } catch (err) {
    console.error("Failed to delete book", err);
    throw err;
  }
};

export const searchBooks = async (query) => {
  if (!query || query.trim() === "") return [];
  try {
    const res = await api.get("/search", {
      params: { q: query }
    });
    return res.data;
  } catch (err) {
    console.error("Search failed", err);
    return [];
  }
};

export const getExternalBook = async (googleId) => {
  if (!googleId) {
    console.warn("getExternalBook called with undefined googleId");
    return null;
  }
  try {
    const res = await api.get(`/search/external/${googleId}`);
    return res.data;
  } catch (err) {
    console.error("Failed to load external book", err);
    throw err;
  }
};