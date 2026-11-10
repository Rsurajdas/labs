import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import type { FetchState, Room } from "../types";
import { getErrorMessage, getRoom } from "../api";

type RoomDetailPageProps = {
  token: string | null;
};

export function RoomDetailPage({ token }: RoomDetailPageProps) {
  const [roomRes, setRoomRes] = useState<FetchState<Room>>({
    status: "loading",
  });
  const params = useParams();
  const roomId = Number(params.roomId);

  if (!Number.isInteger(roomId) || roomId <= 0) {
    return <p>Invalid room id</p>;
  }

  useEffect(() => {
    let ignore = false;

    setRoomRes({ status: "loading" });

    getRoom(roomId)
      .then((data) => {
        if (ignore) return;
        setRoomRes({ status: "success", data });
      })
      .catch((e: unknown) => {
        if (ignore) return;
        setRoomRes({ status: "error", message: getErrorMessage(e) });
      });

    return () => {
      ignore = true;
    };
  }, [roomId]);

  if (roomRes.status === "loading") {
    return <p>Loading room…</p>;
  }

  if (roomRes.status === "error") {
    return <p role="alert">{roomRes.message}</p>;
  }

  return (
    <>
      <h2>{roomRes.data.name}</h2>
      <p>Capacity: {roomRes.data.capacity}</p>

      {!token ? (
        <p>
          Please <Link to="/login">log in</Link> to book this room.
        </p>
      ) : null}
    </>
  );
}
