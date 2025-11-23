import { useEffect, useState } from "react";

const API_URL = "http://localhost:5000";

interface Todo {
  id: number;
  title: string;
  done: boolean;
}

export default function App() {
  const [view, setView] = useState("login"); // login | register | todos
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [token, setToken] = useState<string | null>(null);

  const [todos, setTodos] = useState<Todo[]>([]);
  const [newTodo, setNewTodo] = useState("");

  useEffect(() => {
    (async () => {
      await fetch(`${API_URL}`).then(res => res.json()).then(data => {
        console.log(data);
      });
    })();
  }, [token]);

  const register = async () => {
    const res = await fetch(`${API_URL}/users`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password })
    });
    if (res.ok) {
      alert("Usuario creado");
      setView("login");
    } else {
      const error = await res.json();
      alert(error.error || "Error al crear usuario");
    }
  };

  const login = async () => {
    const res = await fetch(`${API_URL}/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password })
    });
    if (!res.ok) {
      const error = await res.json();
      return alert(error.error || "Credenciales inválidas");
    }

    const data = await res.json();
    setToken(data.token);
    setView("todos");
    loadTodos(data.token);
  };

  const loadTodos = async (authToken: string) => {
    const res = await fetch(`${API_URL}/todos`, {
      headers: { Authorization: authToken }
    });
    if (res.ok) {
      const data: Todo[] = await res.json();
      setTodos(data);
    } else {
      alert("Error al cargar los TODOs");
    }
  };

  const addTodo = async () => {
    if (!newTodo.trim() || !token) return;

    const res = await fetch(`${API_URL}/todos`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: token
      },
      body: JSON.stringify({ title: newTodo })
    });

    if (res.ok) {
      setNewTodo("");
      loadTodos(token);
    } else {
      alert("Error al agregar TODO");
    }
  };

  const toggleDone = async (todo: Todo) => {
    if (!token) return;

    const res = await fetch(`${API_URL}/todos/${todo.id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
        Authorization: token
      },
      body: JSON.stringify({ done: !todo.done })
    });

    if (res.ok) {
      loadTodos(token);
    } else {
      alert("Error al actualizar TODO");
    }
  };

  const deleteTodo = async (todo: Todo) => {
    if (!token) return;

    const res = await fetch(`${API_URL}/todos/${todo.id}`, {
      method: "DELETE",
      headers: { Authorization: token }
    });

    if (res.ok) {
      loadTodos(token);
    } else {
      alert("Error al eliminar TODO");
    }
  };

  // ---------------- RENDER ----------------

  if (view === "login") {
    return (
      <div className="p-6 max-w-md mx-auto">
        <h1 className="text-2xl font-bold mb-4">Login</h1>
        <input className="border p-2 w-full mb-2" placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} />
        <input className="border p-2 w-full mb-4" placeholder="Password" type="password" value={password} onChange={e => setPassword(e.target.value)} />
        <button className="bg-blue-600 text-white px-4 py-2 w-full mb-2" onClick={login}>Ingresar</button>
        <button className="text-blue-600 w-full" onClick={() => setView("register")}>Crear cuenta</button>
      </div>
    );
  }

  if (view === "register") {
    return (
      <div className="p-6 max-w-md mx-auto">
        <h1 className="text-2xl font-bold mb-4">Registrar</h1>
        <input className="border p-2 w-full mb-2" placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} />
        <input className="border p-2 w-full mb-4" placeholder="Password" type="password" value={password} onChange={e => setPassword(e.target.value)} />
        <button className="bg-green-600 text-white px-4 py-2 w-full mb-2" onClick={register}>Crear cuenta</button>
        <button className="text-blue-600 w-full" onClick={() => setView("login")}>Volver al login</button>
      </div>
    );
  }

  return (
    <div className="p-6 max-w-md mx-auto">
      <h1 className="text-2xl font-bold mb-4">Mis TODOs</h1>
      <div className="flex gap-2 mb-4">
        <input className="border p-2 flex-1" placeholder="Nuevo TODO" value={newTodo} onChange={e => setNewTodo(e.target.value)} />
        <button className="bg-blue-600 text-white px-4" onClick={addTodo}>+</button>
      </div>

      <ul className="space-y-2">
        {todos.map(todo => (
          <li key={todo.id} className="border p-3 flex justify-between items-center">
            <span onClick={() => toggleDone(todo)} className={todo.done ? "line-through cursor-pointer" : "cursor-pointer"}>
              {todo.title}
            </span>
            <button className="text-red-600" onClick={() => deleteTodo(todo)}>X</button>
          </li>
        ))}
      </ul>
    </div>
  );
}
