"use client"

import { useState, useEffect } from "react"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { ThemeProvider } from "@/components/theme-provider"
import { ThemeToggle } from "@/components/theme-toggle"
import { RecordTab } from "@/components/tabs/record-tab"
import { ElementSelectorTab } from "@/components/tabs/element-selector-tab"
import { WorkflowBuilderTab } from "@/components/tabs/workflow-builder-tab"
import { ExecutionTab } from "@/components/tabs/execution-tab"
import { TopNavigation } from "@/components/top-navigation"
import { StatusBar } from "@/components/status-bar"
import { Toaster } from "@/components/ui/toaster"
import { motion } from "framer-motion"
import { Sparkles } from "lucide-react"

export default function AutoClickApp() {
  const [activeTab, setActiveTab] = useState("record")
  const [statusMessage, setStatusMessage] = useState("Ready to rock! 🤘")
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  if (!mounted) return null

  return (
    <ThemeProvider defaultTheme="dark" attribute="class">
      <div className="flex flex-col h-screen">
        <TopNavigation />
        <div className="flex-1 container mx-auto p-4 overflow-hidden flex flex-col">
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="flex justify-between items-center mb-6"
          >
            <div className="flex items-center">
              <motion.div
                animate={{
                  rotate: [0, 5, 0, -5, 0],
                }}
                transition={{
                  repeat: Number.POSITIVE_INFINITY,
                  duration: 5,
                  ease: "easeInOut",
                }}
              >
                <Sparkles className="h-8 w-8 mr-3 text-yellow-400" />
              </motion.div>
              <div>
                <h1 className="text-4xl font-black bg-gradient-to-r from-cyan-400 via-fuchsia-500 to-orange-500 text-transparent bg-clip-text">
                  AUTOCLICK
                </h1>
                <p className="text-xs font-medium text-purple-300 tracking-widest uppercase">
                  Web Automation with Attitude
                </p>
              </div>
            </div>
            <ThemeToggle />
          </motion.div>

          <Tabs defaultValue="record" value={activeTab} onValueChange={setActiveTab} className="flex-1 flex flex-col">
            <TabsList className="grid grid-cols-4 mb-6 p-1 bg-background/20 backdrop-blur-md border border-white/10 rounded-xl">
              {["record", "element-selector", "workflow-builder", "execution"].map((tab, index) => (
                <motion.div key={tab} whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                  <TabsTrigger
                    value={tab}
                    className={`py-3 ${activeTab === tab ? "text-white" : "text-white/60"} font-medium transition-all duration-300 data-[state=active]:bg-gradient-to-r data-[state=active]:from-cyan-500 data-[state=active]:to-fuchsia-500 data-[state=active]:shadow-lg data-[state=active]:shadow-purple-500/20 rounded-lg`}
                  >
                    {tab
                      .split("-")
                      .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
                      .join(" ")}
                  </TabsTrigger>
                </motion.div>
              ))}
            </TabsList>

            <div className="flex-1 overflow-hidden">
              <TabsContent value="record" className="h-full">
                <RecordTab setStatusMessage={setStatusMessage} />
              </TabsContent>

              <TabsContent value="element-selector" className="h-full">
                <ElementSelectorTab setStatusMessage={setStatusMessage} />
              </TabsContent>

              <TabsContent value="workflow-builder" className="h-full">
                <WorkflowBuilderTab setStatusMessage={setStatusMessage} />
              </TabsContent>

              <TabsContent value="execution" className="h-full">
                <ExecutionTab setStatusMessage={setStatusMessage} />
              </TabsContent>
            </div>
          </Tabs>
        </div>

        <StatusBar message={statusMessage} />
        <Toaster />
      </div>
    </ThemeProvider>
  )
}

