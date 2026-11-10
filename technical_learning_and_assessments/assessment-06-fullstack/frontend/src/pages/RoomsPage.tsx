import { useEffect, useMemo, useState, type ChangeEvent } from "react";
import type { FetchState, Room } from "../types";
import { getErrorMessage, getRooms } from "../api";
import { Link } from "react-router-dom";

export function RoomsPage() {
  const [roomState, setRoomState] = useState<FetchState<Room[]>>({
    status: "loading",
  });
  const [minCapacity, setMinCapacity] = useState("");

  useEffect(() => {
    let ignore = false;
    getRooms()
      .then((data) => {
        if (ignore) return;
        setRoomState({ status: "success", data });
      })
      .catch((e: unknown) => {
        if (ignore) return;
        setRoomState({ status: "error", message: getErrorMessage(e) });
      });

    return () => {
      ignore = true;
    };
  }, []);

  const rooms = roomState.status === "success" ? roomState.data : [];

  const modifiedRooms = useMemo(() => {
    if (!minCapacity) {
      return [...rooms].sort((a, b) => a.name.localeCompare(b.name));
    }
    return [...rooms]
      .filter((r) => r.capacity >= Number(minCapacity))
      .sort((a, b) => a.name.localeCompare(b.name));
  }, [rooms, minCapacity]);

  if (roomState.status === "loading") {
    return <p>Loading rooms…</p>;
  }

  if (roomState.status === "error") {
    return <p role="alert">{roomState.message}</p>;
  }

  // console.log({ modifiedRooms });

  return (
    <>
      <label htmlFor="minCapacity">Minimum capacity</label>
      <input
        id="minCapacity"
        name="minCapacity"
        type="number"
        min={1}
        value={minCapacity}
        onChange={(e: ChangeEvent<HTMLInputElement>) => {
          setMinCapacity(e.target.value);
        }}
      />
      {!modifiedRooms.length ? (
        <p>No rooms match</p>
      ) : (
        <ul>
          {modifiedRooms.map((room) => (
            <li key={room.id}>
              <Link to={`/rooms/${room.id}`}>
                {room.name} (capacity {room.capacity})
              </Link>
            </li>
          ))}
        </ul>
      )}
    </>
  );
}
