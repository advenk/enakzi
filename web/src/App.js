import React, { useState, useEffect } from "react";
import InfiniteScroll from "react-infinite-scroll-component";
import Masonry from 'react-masonry-css';

function App() {
  const [images, setImages] = useState([]);
  const [offset, setOffset] = useState(0);
  const [loading, setLoading] = useState(true);

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
  }, []);

  const fetchImages = async () => {
    try {
      const response = await fetch(
        `${API_BASE}/images?limit=${LIMIT}&offset=${offset}&sort_by=score&order=desc`
      );
      const newData = await response.json();
      
      // filter out duplicates
      setImages((prev) => {
        const existingIds = new Set(prev.map(img => img.id));
        const uniqueNewImages = newData.filter(img => !existingIds.has(img.id));
        return [...prev, ...uniqueNewImages];
      });
      
      setOffset((prev) => prev + LIMIT);
      setLoading(false);
    } catch (error) {
      console.error("Error fetching images:", error);
      setLoading(false);
    }
  };

  const handleImageClick = (sourceUrl) => {
    if (sourceUrl) {
      window.open(sourceUrl, "_blank");
    }
  };

  const handleImageError = (id) => {
    setImages(prevImages => prevImages.filter(img => img.id !== id));
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3">
          <div className="flex justify-between items-center">
            <h1 className="text-3xl font-bold text-gray-900">expl0rer</h1>
          </div>
        </div>
      </header>

      {/* Main content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
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
                <div 
                  key={img.id} 
                  className="image-card animate-fade-in cursor-pointer transform transition-all duration-300 hover:scale-[1.02]"
                  onClick={() => handleImageClick(img.source_url)}
                >
                  <img
                    src={`${API_BASE}${img.url}`}
                    alt={img.caption || "Explore image"}
                    loading="lazy"
                    onError={() => handleImageError(img.id)}
                  />
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