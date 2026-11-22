import axios from "axios";
import type { Post, Comment } from "./types";

export const api = axios.create({
  baseURL: "https://jsonplaceholder.typicode.com",
  timeout: 15000,
});

export async function fetchPosts(
  maxPostPerPage: number,
  pageNum = 1,
): Promise<Post[]> {
  const response = await api.get<Post[]>(
    `https://jsonplaceholder.typicode.com/posts?_limit=${maxPostPerPage}&_page=${pageNum}`,
  );
  return response.data;
}

export async function fetchComments(postId: number): Promise<Comment[]> {
  const response = await api.get<Comment[]>(
    `https://jsonplaceholder.typicode.com/comments?postId=${postId}`,
  );
  return response.data;
}

export async function deletePost(postId: number): Promise<void> {
  await api.delete(`https://jsonplaceholder.typicode.com/posts/${postId}`);
}

export async function updatePost(postId: number): Promise<Post> {
  const response = await api.patch<Post>(
    `https://jsonplaceholder.typicode.com/posts/${postId}`,
    { title: "REACT QUERY FOREVER!!!!" },
  );
  return response.data;
}
