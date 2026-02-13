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
          className="rounded-xl border border-white/10 bg-gradient-to-br from-[#1a1a28]/90 to-[#12121a]/90 backdrop-blur-sm p-5 shadow-lg animate-pulse"
        >
          <div className="flex items-start gap-4">
            {/* Checkbox skeleton */}
            <div className="mt-1 h-6 w-6 rounded-lg border-2 border-gray-700 bg-gray-800/50" />

            {/* Content skeleton */}
            <div className="flex-1 space-y-3">
              {/* Title skeleton */}
              <div className="h-5 w-3/4 rounded-lg bg-gradient-to-r from-gray-800 via-gray-700 to-gray-800 bg-[length:200%_100%] animate-[shimmer_2s_infinite]" />

              {/* Description skeleton */}
              <div className="space-y-2">
                <div className="h-4 w-full rounded-lg bg-gradient-to-r from-gray-800 via-gray-700 to-gray-800 bg-[length:200%_100%] animate-[shimmer_2s_infinite_0.2s]" />
                <div className="h-4 w-2/3 rounded-lg bg-gradient-to-r from-gray-800 via-gray-700 to-gray-800 bg-[length:200%_100%] animate-[shimmer_2s_infinite_0.4s]" />
              </div>

              {/* Date skeleton */}
              <div className="h-3 w-32 rounded-lg bg-gradient-to-r from-gray-800 via-gray-700 to-gray-800 bg-[length:200%_100%] animate-[shimmer_2s_infinite_0.6s]" />
            </div>

            {/* Action buttons skeleton */}
            <div className="flex gap-2">
              <div className="h-9 w-9 rounded-lg bg-gray-800/50" />
              <div className="h-9 w-9 rounded-lg bg-gray-800/50" />
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
