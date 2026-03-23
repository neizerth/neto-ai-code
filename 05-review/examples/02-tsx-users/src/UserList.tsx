import { useEffect, useState } from "react";

type User = { id: string; name: string };

export function UserList() {
  const [users, setUsers] = useState<User[]>([]);
  const [query, setQuery] = useState("");

  useEffect(() => {
    fetch(`/api/users?q=${encodeURIComponent(query)}`)
      .then((r) => r.json())
      .then((data) => setUsers(data.items ?? []));
  }, [query]);

  return (
    <>
      <input value={query} onChange={(e) => setQuery(e.target.value)} />
      <ul>{users.map((u) => <li key={u.id}>{u.name}</li>)}</ul>
    </>
  );
}
