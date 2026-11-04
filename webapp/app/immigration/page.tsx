import MapBase from "@/components/map";
import Navbar from "@/components/Navbar";

export default function Home() {
    return (
      <main>
        <Navbar />
        <h1>Immigration</h1>
        <p>
          Lorem ipsum...
        </p>
        <iframe
          src="/immigration/dataviz"
          title="Immigration"
          allow-scripts="true"
          allow="fullscreen *"
          style={{ border: 0, width: "100vw", height: "50vh" }}
        />
      </main>
  );
}
