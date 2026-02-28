import { useState, useEffect } from "react";
import reactLogo from "./assets/react.svg";
import "./App.css";

function App() {
  const [count, setCount] = useState(0);
  const [currentTime, setCurrentTime] = useState(0);
  useEffect(() => {
    fetch("/api/time")
      .then((res) => res.json())
      .then((data) => {
        setCurrentTime(data.time);
      });
  }, []);
  return (
    <>
      <header className="w-full bg-[#835432] [--nav-height:3] h-[calc(var(--block-size)_*_var(--nav-height))] md:[--nav-height:2]">
        <div className="h-full w-full bg-[url('/textures/grass-side.png')] bg-repeat-x">
          <div className="flex flex-col md:flex-row items-center justify-end h-full w-full p-5 pt-0 md:pb-0 bg-cover bg-gradient-to-t from-[rgba(0,0,0,0.75)] to-[rgba(0,0,0,0.25)]">
            <a
              href="/"
              className="h-auto w-[1.5rem] md:w-[2.25rem] mx-auto md:ml-0"
            >
              <img src="/imgs/logo.png" alt="logo" className="" />
            </a>
            <nav className="flex items-center justify-end w-full md:w-min gap-3 text-2xl text-white">
              {children}
              <a href="/" className="hover:underline">
                Home
              </a>
              <a href="/docs" className="hover:underline">
                Docs
              </a>
              <a
                href="https://github.com/..."
                className="border-2 border-[#3a3a3a] bg-[#5a5a5a] hover:bg-[#7a7a7a] py-1 px-2 text-lg"
                target="_blank"
              >
                Github
              </a>
            </nav>
          </div>
        </div>
      </header>
    </>
  );
}

export default App;
