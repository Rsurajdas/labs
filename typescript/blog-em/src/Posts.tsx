import { useState } from "react";

import { fetchPosts } from "./api";
import { PostDetail } from "./PostDetail";
import type { Post } from "./types";
import { useQuery } from "@tanstack/react-query";
const maxPostPage = 20;

export function Posts() {
  const [currentPage, setCurrentPage] = useState(0);
  const [selectedPost, setSelectedPost] = useState<Post | null>(null);

  const { data, isError, isLoading } = useQuery<Post[]>({
    queryKey: ["posts", currentPage],
    queryFn: () => fetchPosts(maxPostPage, currentPage + 1),
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
            onClick={() => setSelectedPost(post)}
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
      {selectedPost ? <PostDetail post={selectedPost} /> : null}
    </>
  );
}
