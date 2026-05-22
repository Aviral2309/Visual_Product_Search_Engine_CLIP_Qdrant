export default function VisualProductSearchFrontend() {
  return (
    <div className="min-h-screen bg-slate-950 text-white p-6">
      <ProductSearchApp />
    </div>
  )
}

import { useEffect, useState } from "react"
import { Search, Loader2, ImageIcon, Sparkles } from "lucide-react"
import { Card, CardContent } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import { Badge } from "@/components/ui/badge"
import { Slider } from "@/components/ui/slider"
import { motion } from "framer-motion"

const API_BASE = "http://127.0.0.1:8000"

function ProductSearchApp() {
  const [query, setQuery] = useState("")
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [topK, setTopK] = useState(5)
  const [health, setHealth] = useState(null)
  const [error, setError] = useState("")

  useEffect(() => {
    fetchHealth()
  }, [])

  async function fetchHealth() {
    try {
      const res = await fetch(`${API_BASE}/health`)
      const data = await res.json()
      setHealth(data)
    } catch (err) {
      console.error(err)
    }
  }

  async function handleSearch(e) {
    e.preventDefault()

    if (!query.trim()) return

    setLoading(true)
    setError("")

    try {
      const res = await fetch(
        `${API_BASE}/search?q=${encodeURIComponent(query)}&top_k=${topK}`
      )

      if (!res.ok) {
        throw new Error("Search failed")
      }

      const data = await res.json()

      setResults(data.results)
    } catch (err) {
      console.error(err)
      setError("Failed to fetch search results")
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-7xl mx-auto">
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-10"
      >
        <div className="flex items-center gap-3 mb-4">
          <div className="p-3 rounded-2xl bg-violet-600">
            <Sparkles className="w-7 h-7" />
          </div>

          <div>
            <h1 className="text-4xl font-bold">
              Visual Product Search Engine
            </h1>

            <p className="text-slate-400 mt-1">
              CLIP + Qdrant Semantic Image Retrieval
            </p>
          </div>
        </div>

        {health && (
          <div className="flex flex-wrap gap-3 mt-6">
            <Badge className="text-sm px-4 py-2 bg-green-600 hover:bg-green-600">
              API Status: {health.status}
            </Badge>

            <Badge className="text-sm px-4 py-2 bg-blue-600 hover:bg-blue-600">
              Indexed Products: {health.total_indexed}
            </Badge>

            <Badge className="text-sm px-4 py-2 bg-purple-600 hover:bg-purple-600">
              {health.model}
            </Badge>
          </div>
        )}
      </motion.div>

      {/* Search Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <Card className="bg-slate-900 border-slate-800 rounded-3xl shadow-2xl mb-10">
          <CardContent className="p-8">
            <form onSubmit={handleSearch} className="space-y-6">
              <div>
                <label className="text-sm text-slate-400 mb-3 block">
                  Search Products
                </label>

                <div className="flex gap-3">
                  <div className="relative flex-1">
                    <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 w-5 h-5" />

                    <Input
                      value={query}
                      onChange={(e) => setQuery(e.target.value)}
                      placeholder="Try: black sneakers, white shirt, blue dress..."
                      className="pl-12 h-14 bg-slate-950 border-slate-700 text-white rounded-2xl text-lg"
                    />
                  </div>

                  <Button
                    type="submit"
                    disabled={loading}
                    className="h-14 px-8 rounded-2xl text-lg bg-violet-600 hover:bg-violet-700"
                  >
                    {loading ? (
                      <>
                        <Loader2 className="w-5 h-5 animate-spin mr-2" />
                        Searching
                      </>
                    ) : (
                      <>
                        <Search className="w-5 h-5 mr-2" />
                        Search
                      </>
                    )}
                  </Button>
                </div>
              </div>

              {/* Slider */}
              <div>
                <div className="flex justify-between mb-3">
                  <span className="text-sm text-slate-400">
                    Number of Results
                  </span>

                  <span className="text-violet-400 font-semibold">
                    {topK}
                  </span>
                </div>

                <Slider
                  value={[topK]}
                  min={1}
                  max={20}
                  step={1}
                  onValueChange={(value) => setTopK(value[0])}
                />
              </div>
            </form>
          </CardContent>
        </Card>
      </motion.div>

      {/* Error */}
      {error && (
        <div className="bg-red-500/10 border border-red-500/20 rounded-2xl p-4 mb-6 text-red-400">
          {error}
        </div>
      )}

      {/* Results */}
      {results.length > 0 && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-2xl font-bold">
              Search Results
            </h2>

            <Badge className="bg-slate-800 text-slate-300 px-4 py-2">
              {results.length} matches
            </Badge>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
            {results.map((item, index) => (
              <motion.div
                key={item.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.05 }}
              >
                <Card className="overflow-hidden rounded-3xl border-slate-800 bg-slate-900 hover:border-violet-500 transition-all duration-300 hover:scale-[1.02] shadow-xl">
                  <div className="aspect-square bg-slate-950 flex items-center justify-center overflow-hidden">
                    <img
                      src={`/${item.image_path}`}
                      alt={item.category}
                      className="w-full h-full object-contain p-4"
                    />
                  </div>

                  <CardContent className="p-5 space-y-4">
                    <div className="flex items-start justify-between gap-3">
                      <div>
                        <h3 className="font-semibold capitalize text-lg">
                          {item.category.replace("_", " ")}
                        </h3>

                        <p className="text-sm text-slate-400 truncate max-w-[180px]">
                          {item.filename}
                        </p>
                      </div>

                      <div className="bg-violet-600 text-white text-xs font-bold px-3 py-2 rounded-xl">
                        {(item.score * 100).toFixed(1)}%
                      </div>
                    </div>

                    <div>
                      <div className="flex justify-between text-sm mb-2 text-slate-400">
                        <span>Similarity</span>
                        <span>{item.score.toFixed(4)}</span>
                      </div>

                      <div className="w-full h-2 bg-slate-800 rounded-full overflow-hidden">
                        <div
                          className="h-full bg-violet-500 rounded-full"
                          style={{ width: `${item.score * 100}%` }}
                        />
                      </div>
                    </div>

                    <div className="flex items-center gap-2">
                      <ImageIcon className="w-4 h-4 text-slate-500" />

                      <span className="text-xs text-slate-500 truncate">
                        {item.image_path}
                      </span>
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            ))}
          </div>
        </motion.div>
      )}

      {/* Empty State */}
      {!loading && results.length === 0 && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="text-center py-24"
        >
          <div className="inline-flex p-6 rounded-full bg-slate-900 mb-6">
            <Search className="w-10 h-10 text-violet-400" />
          </div>

          <h3 className="text-2xl font-semibold mb-3">
            Search for Products
          </h3>

          <p className="text-slate-400 max-w-xl mx-auto text-lg">
            Enter natural language queries like
            "black shoes", "white shirt", or
            "blue dress" to retrieve visually
            similar products using CLIP embeddings.
          </p>
        </motion.div>
      )}
    </div>
  )
}
