/**
 * TaskListSkeleton Component
 *
 * Loading skeleton for task list
 */

export default function TaskListSkeleton() {
  return (
    <div className="space-y-3">
      {[1, 2, 3].map((i) => (
        <div
          key={i}
          className="animate-pulse rounded-lg border border-gray-200 bg-white p-4 shadow-sm"
        >
          <div className="flex items-start gap-3">
            <div className="h-5 w-5 rounded border-2 border-gray-300" />
            <div className="flex-1 space-y-2">
              <div className="h-4 w-3/4 rounded bg-gray-200" />
              <div className="h-3 w-1/2 rounded bg-gray-200" />
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
