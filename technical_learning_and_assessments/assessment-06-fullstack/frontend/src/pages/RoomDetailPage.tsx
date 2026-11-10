import { useEffect, useState, type SubmitEvent } from "react";
import { Link, useParams } from "react-router-dom";
import type { FetchState, NewBooking, Room } from "../types";
import { getErrorMessage, getRoom } from "../api";

type RoomDetailPageProps = {
  token: string | null;
};

export function RoomDetailPage({ token }: RoomDetailPageProps) {
  const [roomRes, setRoomRes] = useState<FetchState<Room>>({
    status: "loading",
  });
  const [errMsg, setErrMsg] = useState("");
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

  function submitHandler(e: SubmitEvent<HTMLFormElement>) {
    e.preventDefault();
    setErrMsg("");
    const formData = new FormData(e.currentTarget);
    const title = String(formData.get("title"));
    if (title.trim().length < 3) {
      setErrMsg("Title must be at least 3 characters");
    }
  }

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
      ) : (
        <form onSubmit={submitHandler}>
          <div>
            <label htmlFor="title">Title</label>
            <input type="text" id="title" name="title" />
          </div>
          <div>
            <label htmlFor="day">Day</label>
            <input type="date" id="day" name="day" />
          </div>
          <div>
            <label htmlFor="slot">Slot</label>
            <select id="slot" name="slot" defaultValue={1}>
              <option value="1">1</option>
              <option value="2">2</option>
              <option value="3">3</option>
              <option value="4">4</option>
              <option value="5">5</option>
              <option value="6">6</option>
              <option value="7">7</option>
              <option value="8">8</option>
            </select>
          </div>
          <button type="submit">Book</button>
          <p role="alert">{errMsg}</p>
        </form>
      )}
    </>
  );
}
