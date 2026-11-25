import { useQuery, type UseMutationResult } from "@tanstack/react-query";
import { fetchComments } from "./api";
import "./PostDetail.css";
import type { Post } from "./types";

type PostDetailProps = {
  post: Post;
  deleteMutation: UseMutationResult<void, Error, number>;
  updateMutation: UseMutationResult<Post, Error, number>;
};

export function PostDetail({
  post,
  deleteMutation,
  updateMutation,
}: PostDetailProps) {
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
        <button onClick={() => updateMutation.mutate(post.id)}>
          Update title
        </button>
        {updateMutation.isPending ? <p>Updating blog title...</p> : null}
        {updateMutation.isSuccess ? <p>Title updated</p> : null}
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
