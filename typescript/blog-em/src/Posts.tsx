import { useCallback, useEffect, useState } from "react";

import { deletePost, fetchPosts } from "./api";
import { PostDetail } from "./PostDetail";
import type { Post } from "./types";
import {
  noop,
  useMutation,
  useQuery,
  useQueryClient,
} from "@tanstack/react-query";
const maxPostPerPage = 5;

export function Posts() {
  const [currentPage, setCurrentPage] = useState(0);
  const [selectedPost, setSelectedPost] = useState<Post | null>(null);
  const queryClient = useQueryClient();
  const deleteMutation = useMutation({
    mutationFn: (postId: number) => deletePost(postId),
  });

  const preFetchPosts = useCallback(async () => {
    const nextPage = currentPage + 1;
    await queryClient
      .query({
        queryKey: ["posts", nextPage],
        queryFn: () => fetchPosts(maxPostPerPage, nextPage),
      })
      .catch(noop);
  }, [currentPage, queryClient]);

  // Pre-fetch next page data
  useEffect(() => {
    preFetchPosts();
  }, [currentPage, queryClient, preFetchPosts]);

  const { data, isError, isLoading } = useQuery<Post[]>({
    queryKey: ["posts", currentPage],
    queryFn: () => fetchPosts(maxPostPerPage, currentPage + 1),
    staleTime: 2000,
  });

  if (isError) {
    return (
      <>
        <h4>Something went wrong!</h4>
      </>
    );
  }

  if (isLoading) {
    return (
      <>
        <h4>Loading...</h4>
      </>
    );
  }

  return (
    <>
      <ul>
        {data?.map((post) => (
          <li
            key={post.id}
            className="post-title"
            onClick={() => {
              deleteMutation.reset();
              setSelectedPost(post);
            }}
          >
            {post.title}
          </li>
        ))}
      </ul>
      <div className="pages">
        <button
          disabled={!currentPage}
          onClick={() => setCurrentPage((cp) => cp - 1)}
        >
          Previous page
        </button>
        <span>Page {currentPage + 1}</span>
        <button onClick={() => setCurrentPage((cp) => cp + 1)}>
          Next page
        </button>
      </div>
      <hr />
      {selectedPost ? (
        <PostDetail post={selectedPost} deleteMutation={deleteMutation} />
      ) : null}
    </>
  );
}
