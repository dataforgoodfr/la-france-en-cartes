import MapBase from "@/components/MapBase";

export default function Home() {
    return (
      <div className="flex flex-col min-h-screen w-screen h-screen">
        <main className="flex-1 w-full h-full">
          <MapBase
          />
        </main>
      </div>
  );
}
