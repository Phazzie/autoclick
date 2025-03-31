"use client"

import { useState } from "react"
import { Crosshair, Copy, Save, RefreshCw, Target, Sparkles } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { useToast } from "@/components/ui/use-toast"
import { Badge } from "@/components/ui/badge"
import { motion, AnimatePresence } from "framer-motion"

type ElementProperty = {
  name: string
  value: string
}

export function ElementSelectorTab({ setStatusMessage }: { setStatusMessage: (message: string) => void }) {
  const [isSelecting, setIsSelecting] = useState(false)
  const [selectedElement, setSelectedElement] = useState<{
    name: string
    properties: ElementProperty[]
    preview: string
    xpath: string
    css: string
  } | null>(null)
  const { toast } = useToast()

  const startElementSelection = () => {
    setIsSelecting(true)
    setStatusMessage("Select an element on the page... 🎯")

    // Simulate selecting an element after a delay
    setTimeout(() => {
      setIsSelecting(false)
      setSelectedElement({
        name: "Button",
        properties: [
          { name: "id", value: "submit-button" },
          { name: "class", value: "btn btn-primary btn-lg" },
          { name: "type", value: "submit" },
          { name: "disabled", value: "false" },
          { name: "aria-label", value: "Submit form" },
          { name: "data-testid", value: "submit-button" },
        ],
        preview: '<button id="submit-button" class="btn btn-primary btn-lg" type="submit">Submit</button>',
        xpath: '//*[@id="form"]/div[3]/button',
        css: "#form > div:nth-child(3) > button",
      })
      setStatusMessage("Element selected! 🎯")
      toast({
        title: "Element selected",
        description: "Button element has been selected",
      })
    }, 2000)
  }

  const copySelector = (selector: string, type: string) => {
    navigator.clipboard.writeText(selector)
    toast({
      title: "Copied to clipboard",
      description: `${type} selector copied`,
    })
  }

  const saveElement = () => {
    if (!selectedElement) return

    toast({
      title: "Element saved",
      description: "Element added to workflow",
    })
    setStatusMessage("Element saved to workflow ✨")
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="h-full grid grid-cols-1 md:grid-cols-2 gap-6"
    >
      <Card className="flex flex-col bg-black/40 backdrop-blur-xl border border-white/10 shadow-xl rounded-xl overflow-hidden">
        <CardContent className="flex flex-col gap-4 p-6 flex-1">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-bold bg-gradient-to-r from-cyan-400 to-purple-400 text-transparent bg-clip-text">
              Element Selector
            </h2>
            <TooltipProvider>
              <Tooltip>
                <TooltipTrigger asChild>
                  <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                    <Button
                      variant={isSelecting ? "secondary" : "default"}
                      size="sm"
                      onClick={startElementSelection}
                      disabled={isSelecting}
                      className={
                        isSelecting
                          ? "bg-amber-500 text-white"
                          : "bg-gradient-to-r from-cyan-500 to-blue-500 text-white border-none shadow-lg shadow-blue-500/30"
                      }
                    >
                      <Crosshair className="h-4 w-4 mr-2" />
                      {isSelecting ? "Selecting..." : "Select Element"}
                    </Button>
                  </motion.div>
                </TooltipTrigger>
                <TooltipContent className="bg-black/80 backdrop-blur-xl border border-white/20 text-white">
                  <p>Click to select an element on the page</p>
                </TooltipContent>
              </Tooltip>
            </TooltipProvider>
          </div>

          <AnimatePresence mode="wait">
            {selectedElement ? (
              <motion.div
                key="element-details"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                className="flex-1 flex flex-col"
              >
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center">
                    <h3 className="text-sm font-medium text-white/80">Selected Element</h3>
                    <Badge
                      variant="outline"
                      className="ml-2 bg-gradient-to-r from-cyan-500 to-blue-500 text-white border-none"
                    >
                      {selectedElement.name}
                    </Badge>
                  </div>
                  <TooltipProvider>
                    <div className="flex gap-2">
                      <Tooltip>
                        <TooltipTrigger asChild>
                          <motion.div whileHover={{ scale: 1.1 }} whileTap={{ scale: 0.9 }}>
                            <Button
                              variant="outline"
                              size="icon"
                              onClick={saveElement}
                              className="bg-white/5 border border-white/20 text-white hover:bg-white/10 rounded-full h-8 w-8"
                            >
                              <Save className="h-4 w-4" />
                              <span className="sr-only">Save element</span>
                            </Button>
                          </motion.div>
                        </TooltipTrigger>
                        <TooltipContent className="bg-black/80 backdrop-blur-xl border border-white/20 text-white">
                          <p>Save element to workflow</p>
                        </TooltipContent>
                      </Tooltip>
                      <Tooltip>
                        <TooltipTrigger asChild>
                          <motion.div whileHover={{ scale: 1.1 }} whileTap={{ scale: 0.9 }}>
                            <Button
                              variant="outline"
                              size="icon"
                              onClick={startElementSelection}
                              className="bg-white/5 border border-white/20 text-white hover:bg-white/10 rounded-full h-8 w-8"
                            >
                              <RefreshCw className="h-4 w-4" />
                              <span className="sr-only">Select new element</span>
                            </Button>
                          </motion.div>
                        </TooltipTrigger>
                        <TooltipContent className="bg-black/80 backdrop-blur-xl border border-white/20 text-white">
                          <p>Select new element</p>
                        </TooltipContent>
                      </Tooltip>
                    </div>
                  </TooltipProvider>
                </div>

                <Tabs defaultValue="properties" className="flex-1 flex flex-col">
                  <TabsList className="grid grid-cols-3 bg-white/5 border border-white/10 p-1">
                    <TabsTrigger
                      value="properties"
                      className="data-[state=active]:bg-gradient-to-r data-[state=active]:from-cyan-500 data-[state=active]:to-blue-500 data-[state=active]:text-white rounded-md"
                    >
                      Properties
                    </TabsTrigger>
                    <TabsTrigger
                      value="selectors"
                      className="data-[state=active]:bg-gradient-to-r data-[state=active]:from-cyan-500 data-[state=active]:to-blue-500 data-[state=active]:text-white rounded-md"
                    >
                      Selectors
                    </TabsTrigger>
                    <TabsTrigger
                      value="preview"
                      className="data-[state=active]:bg-gradient-to-r data-[state=active]:from-cyan-500 data-[state=active]:to-blue-500 data-[state=active]:text-white rounded-md"
                    >
                      Preview
                    </TabsTrigger>
                  </TabsList>

                  <div className="flex-1 mt-3">
                    <TabsContent value="properties" className="h-full">
                      <ScrollArea className="h-full border border-white/10 rounded-lg bg-black/20">
                        <div className="p-4">
                          <table className="w-full text-sm">
                            <thead>
                              <tr className="border-b border-white/10">
                                <th className="text-left py-2 font-medium text-white/80">Property</th>
                                <th className="text-left py-2 font-medium text-white/80">Value</th>
                              </tr>
                            </thead>
                            <tbody>
                              {selectedElement.properties.map((prop, index) => (
                                <motion.tr
                                  key={index}
                                  className="border-b border-white/10"
                                  initial={{ opacity: 0, y: 10 }}
                                  animate={{ opacity: 1, y: 0 }}
                                  transition={{ delay: index * 0.05 }}
                                >
                                  <td className="py-2 font-mono text-xs text-cyan-300">{prop.name}</td>
                                  <td className="py-2 font-mono text-xs text-purple-300">{prop.value}</td>
                                </motion.tr>
                              ))}
                            </tbody>
                          </table>
                        </div>
                      </ScrollArea>
                    </TabsContent>

                    <TabsContent value="selectors" className="h-full">
                      <ScrollArea className="h-full border border-white/10 rounded-lg bg-black/20">
                        <div className="p-4 space-y-4">
                          <div>
                            <div className="flex items-center justify-between mb-2">
                              <h4 className="text-sm font-medium text-white/80">XPath</h4>
                              <Button
                                variant="ghost"
                                size="sm"
                                className="h-6 px-2 text-cyan-400 hover:text-cyan-300 hover:bg-white/5"
                                onClick={() => copySelector(selectedElement.xpath, "XPath")}
                              >
                                <Copy className="h-3 w-3 mr-1" /> Copy
                              </Button>
                            </div>
                            <div className="bg-black/30 p-3 rounded-md font-mono text-xs overflow-x-auto border border-white/10 text-cyan-300">
                              {selectedElement.xpath}
                            </div>
                          </div>

                          <div>
                            <div className="flex items-center justify-between mb-2">
                              <h4 className="text-sm font-medium text-white/80">CSS Selector</h4>
                              <Button
                                variant="ghost"
                                size="sm"
                                className="h-6 px-2 text-cyan-400 hover:text-cyan-300 hover:bg-white/5"
                                onClick={() => copySelector(selectedElement.css, "CSS")}
                              >
                                <Copy className="h-3 w-3 mr-1" /> Copy
                              </Button>
                            </div>
                            <div className="bg-black/30 p-3 rounded-md font-mono text-xs overflow-x-auto border border-white/10 text-purple-300">
                              {selectedElement.css}
                            </div>
                          </div>
                        </div>
                      </ScrollArea>
                    </TabsContent>

                    <TabsContent value="preview" className="h-full">
                      <ScrollArea className="h-full border border-white/10 rounded-lg bg-black/20">
                        <div className="p-4">
                          <h4 className="text-sm font-medium mb-2 text-white/80">Element HTML</h4>
                          <div className="bg-black/30 p-3 rounded-md font-mono text-xs overflow-x-auto whitespace-pre-wrap border border-white/10 text-cyan-300">
                            {selectedElement.preview}
                          </div>

                          <h4 className="text-sm font-medium mt-4 mb-2 text-white/80">Visual Preview</h4>
                          <div className="border border-white/10 rounded-md p-6 flex items-center justify-center bg-black/20">
                            <motion.button
                              whileHover={{ scale: 1.05 }}
                              whileTap={{ scale: 0.95 }}
                              className="px-4 py-2 bg-gradient-to-r from-blue-600 to-indigo-600 text-white rounded-md font-medium shadow-lg shadow-blue-500/30"
                            >
                              Submit
                            </motion.button>
                          </div>
                        </div>
                      </ScrollArea>
                    </TabsContent>
                  </div>
                </Tabs>
              </motion.div>
            ) : (
              <motion.div
                key="element-empty"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="flex-1 flex items-center justify-center border border-white/10 rounded-lg bg-black/20"
              >
                <div className="text-center p-6">
                  <motion.div
                    animate={{
                      scale: [1, 1.05, 1],
                      rotate: [0, 5, 0, -5, 0],
                    }}
                    transition={{
                      repeat: Number.POSITIVE_INFINITY,
                      duration: 5,
                      ease: "easeInOut",
                    }}
                  >
                    <div className="w-20 h-20 mx-auto mb-4 rounded-full bg-gradient-to-r from-cyan-500 to-blue-500 flex items-center justify-center shadow-lg shadow-blue-500/30">
                      <Target className="h-10 w-10 text-white" />
                    </div>
                  </motion.div>
                  <p className="text-white/80 text-lg font-medium">
                    {isSelecting ? "Click on an element in the browser..." : "Click 'Select Element' to begin"}
                  </p>
                  <p className="text-sm text-white/60 mt-2">Element properties will appear here</p>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </CardContent>
      </Card>

      <Card className="flex flex-col bg-black/40 backdrop-blur-xl border border-white/10 shadow-xl rounded-xl overflow-hidden">
        <CardContent className="p-6 flex-1">
          <h2 className="text-xl font-bold bg-gradient-to-r from-cyan-400 to-purple-400 text-transparent bg-clip-text mb-4">
            Browser Preview
          </h2>
          <div className="border border-white/10 rounded-lg h-[calc(100%-2rem)] flex items-center justify-center bg-black/30 relative overflow-hidden">
            {isSelecting && (
              <div className="absolute top-4 right-4 z-10">
                <div className="flex items-center gap-2 bg-gradient-to-r from-cyan-500 to-blue-500 text-white px-3 py-1.5 rounded-full text-sm font-medium shadow-lg shadow-blue-500/30">
                  <Crosshair className="h-4 w-4" />
                  Element Selection Mode
                </div>
              </div>
            )}

            <div className="absolute inset-0 pointer-events-none">
              <div className="absolute inset-0 bg-[url('/grid.svg')] bg-center opacity-10"></div>
              {isSelecting && (
                <div className="absolute inset-0 bg-gradient-to-r from-cyan-500/10 to-blue-500/10 animate-pulse"></div>
              )}
            </div>

            <div className="text-center p-4 relative z-0">
              <motion.div
                animate={{
                  scale: [1, 1.05, 1],
                  rotate: [0, 2, 0, -2, 0],
                }}
                transition={{
                  repeat: Number.POSITIVE_INFINITY,
                  duration: 5,
                  ease: "easeInOut",
                }}
                className="w-24 h-24 mx-auto mb-6 rounded-full bg-gradient-to-r from-cyan-500 via-blue-500 to-purple-500 flex items-center justify-center shadow-xl shadow-blue-500/30"
              >
                <Sparkles className="h-12 w-12 text-white" />
              </motion.div>
              <p className="text-white/80 text-lg font-medium">
                {isSelecting
                  ? "Hover over elements to highlight them, click to select"
                  : "Click 'Select Element' to begin selecting elements"}
              </p>
              <p className="text-sm text-white/60 mt-2">The browser window will appear here when connected</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  )
}

