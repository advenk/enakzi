import React, { useState, useEffect } from "react";
import InfiniteScroll from "react-infinite-scroll-component";
import Masonry from 'react-masonry-css';
import { ArrowTopRightOnSquareIcon, ShareIcon } from '@heroicons/react/24/outline';

function App() {
  const [images, setImages] = useState([]);
  const [offset, setOffset] = useState(0);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [sortBy, setSortBy] = useState("score");
  const [order, setOrder] = useState("desc");

  const API_BASE = process.env.REACT_APP_API_URL || "http://localhost:8000";
  const LIMIT = 20;

  const breakpointColumns = {
    default: 4,
    1536: 4,
    1280: 3,
    1024: 3,
    768: 2,
    640: 1
  };

  useEffect(() => {
    fetchImages();
    fetchStats();
    // eslint-disable-next-line
  }, [sortBy, order]);

  const fetchImages = async () => {
    try {
      const response = await fetch(
        `${API_BASE}/images?limit=${LIMIT}&offset=${offset}&sort_by=${sortBy}&order=${order}`
      );
      const newData = await response.json();
      setImages((prev) => [...prev, ...newData]);
      setOffset((prev) => prev + LIMIT);
      setLoading(false);
    } catch (error) {
      console.error("Error fetching images:", error);
      setLoading(false);
    }
  };

  const fetchStats = async () => {
    try {
      const response = await fetch(`${API_BASE}/stats`);
      const data = await response.json();
      setStats(data);
    } catch (error) {
      console.error("Error fetching stats:", error);
    }
  };

  const getScoreBadgeClass = (score) => {
    if (score >= 9) return "score-badge score-excellent";
    if (score >= 7) return "score-badge score-good";
    return "score-badge score-average";
  };

  const handleShare = (image) => {
    const shareUrl = `${window.location.origin}${image.url}`;
    const shareText = image.caption || "Check out this amazing image from expl0rer";
    
    if (navigator.share) {
      navigator.share({
        title: "expl0rer Image",
        text: shareText,
        url: shareUrl,
      });
    } else {
      window.open(
        `https://twitter.com/intent/tweet?url=${encodeURIComponent(
          shareUrl
        )}&text=${encodeURIComponent(shareText)}`,
        "_blank"
      );
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex justify-between items-center">
            <h1 className="text-3xl font-bold text-gray-900">expl0rer</h1>
            
            {stats && (
              <div className="text-sm text-gray-600">
                <span className="mr-4">Total Images: {stats.total_images}</span>
                <span>Avg Score: {stats.average_score}</span>
              </div>
            )}

            <div className="flex space-x-4">
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
              >
                <option value="score">Sort by Score</option>
                <option value="timestamp">Sort by Date</option>
              </select>
              
              <select
                value={order}
                onChange={(e) => setOrder(e.target.value)}
                className="rounded-md border-gray-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
              >
                <option value="desc">Descending</option>
                <option value="asc">Ascending</option>
              </select>
            </div>
          </div>
        </div>
      </header>

      {/* Main content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {loading ? (
          <div className="flex justify-center items-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
          </div>
        ) : (
          <InfiniteScroll
            dataLength={images.length}
            next={fetchImages}
            hasMore={true}
            loader={
              <div className="flex justify-center py-4">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
              </div>
            }
          >
            <Masonry
              breakpointCols={breakpointColumns}
              className="masonry-grid"
              columnClassName="masonry-grid_column"
            >
              {images.map((img) => (
                <div key={img.id} className="image-card animate-fade-in">
                  <img
                    src={`${API_BASE}${img.url}`}
                    alt={img.caption}
                    loading="lazy"
                  />
                  <div className="image-info">
                    <div className="flex justify-between items-start mb-2">
                      <span className={getScoreBadgeClass(img.score)}>
                        Score: {img.score.toFixed(2)}
                      </span>
                      <div className="flex space-x-2">
                        <button
                          onClick={() => window.open(img.source_url, "_blank")}
                          className="p-1 rounded-full hover:bg-gray-100"
                          title="Open source"
                        >
                          <ArrowTopRightOnSquareIcon className="h-5 w-5 text-gray-500" />
                        </button>
                        <button
                          onClick={() => handleShare(img)}
                          className="p-1 rounded-full hover:bg-gray-100"
                          title="Share"
                        >
                          <ShareIcon className="h-5 w-5 text-gray-500" />
                        </button>
                      </div>
                    </div>
                    {img.caption && (
                      <p className="text-sm text-gray-600 line-clamp-2">
                        {img.caption}
                      </p>
                    )}
                  </div>
                </div>
              ))}
            </Masonry>
          </InfiniteScroll>
        )}
      </main>
    </div>
  );
}

export default App; 