export default function LoadingState() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-neutral-50">
      <div className="text-center">
        <div className="inline-block w-8 h-8 border-2 border-neutral-300 border-t-neutral-900 rounded-full animate-spin mb-4" />
        <p className="text-neutral-600">Cloning and indexing your repository...</p>
        <p className="text-sm text-neutral-500 mt-2">This may take a few minutes</p>
      </div>
    </div>
  );
}
