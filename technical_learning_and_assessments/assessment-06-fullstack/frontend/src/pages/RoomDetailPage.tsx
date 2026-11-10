import { useParams } from "react-router-dom";

type RoomDetailPageProps = {
  token: string | null;
};

export function RoomDetailPage({}: RoomDetailPageProps) {
  const params = useParams();
  const roomId = Number(params.roomId);

  if (!Number.isInteger(roomId) || roomId <= 0) {
    return <p>Invalid room id</p>;
  }

  return <div>RoomDetailPage</div>;
}
