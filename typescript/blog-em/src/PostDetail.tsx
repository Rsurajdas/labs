import { useQuery, type UseMutationResult } from "@tanstack/react-query";
// eslint-disable-next-line @typescript-eslint/no-unused-vars
import { fetchComments } from "./api";
import "./PostDetail.css";
import type { Post } from "./types";

type PostDetailProps = {
  post: Post;
  deleteMutation: UseMutationResult<void, Error, number>;
};

export function PostDetail({ post, deleteMutation }: PostDetailProps) {
  const { data, isError, isLoading } = useQuery({
    queryKey: ["comments", post.id],
    queryFn: () => fetchComments(post.id),
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
      <h3 style={{ color: "blue" }}>{post.title}</h3>
      <div>
        <button onClick={() => deleteMutation.mutate(post.id)}>Delete</button>
        {deleteMutation.isPending ? <p>Blog is deleting...</p> : null}
        {deleteMutation.isSuccess ? <p>Blog is deleted</p> : null}
      </div>
      <div>
        <button onClick={() => {}}>Update title</button>
      </div>
      <p>{post.body}</p>
      <h4>Comments</h4>
      {data?.map((comment) => (
        <li key={comment.id}>
          {comment.email}: {comment.body}
        </li>
      ))}
    </>
  );
}
