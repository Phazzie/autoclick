"use client"

import { useState, useEffect } from "react"
import {
  Play,
  Pause,
  StopCircle,
  Clock,
  Calendar,
  CheckCircle2,
  XCircle,
  AlertCircle,
  RefreshCw,
  Zap,
  Flame,
} from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"
import { useToast } from "@/components/ui/use-toast"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion"
import { Badge } from "@/components/ui/badge"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { motion, AnimatePresence } from "framer-motion"

type LogEntry = {
  id: string
  timestamp: Date
  level: "info" | "warning" | "error" | "success"
  message: string
  details?: string
}

type ExecutionResult = {
  id: string
  stepName: string
  status: "success" | "error" | "skipped"
  duration: number
  message?: string
}

export function ExecutionTab({ setStatusMessage }: { setStatusMessage: (message: string) => void }) {
  const [isRunning, setIsRunning] = useState(false)
  const [isPaused, setIsPaused] = useState(false)
  const [progress, setProgress] = useState(0)
  const [selectedWorkflow, setSelectedWorkflow] = useState("login-workflow")
  const [logs, setLogs] = useState<LogEntry[]>([])
  const [results, setResults] = useState<ExecutionResult[]>([])
  const { toast } = useToast()
  const [countdown, setCountdown] = useState<number | null>(null)

  useEffect(() => {
    if (countdown !== null && countdown > 0) {
      const timer = setTimeout(() => setCountdown(countdown - 1), 1000)
      return () => clearTimeout(timer)
    } else if (countdown === 0) {
      setCountdown(null)
      startActualExecution()
    }
  }, [countdown])

  const startExecution = () => {
    if (isPaused) {
      setIsPaused(false)
      toast({
        title: "Execution resumed",
        description: "Workflow execution has been resumed",
      })
      setStatusMessage("Execution resumed ▶️")
      return
    }

    setCountdown(3)
    setStatusMessage("Preparing to execute workflow... ⚡")
    toast({
      title: "Execution starting in 3...",
      description: "Prepare for workflow execution",
    })
  }

  const startActualExecution = () => {
    setIsRunning(true)
    setProgress(0)
    setLogs([])
    setResults([])

    toast({
      title: "Execution started",
      description: `Running "${selectedWorkflow}"`,
    })
    setStatusMessage(`Running "${selectedWorkflow}" 🚀`)

    // Simulate execution progress
    const interval = setInterval(() => {
      setProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval)
          setIsRunning(false)

          toast({
            title: "Execution completed",
            description: "Workflow execution has completed",
          })
          setStatusMessage("Execution completed ✅")

          return 100
        }
        return prev + 20
      })

      // Add log entries
      const newLog: LogEntry = {
        id: `log-${Date.now()}`,
        timestamp: new Date(),
        level: Math.random() > 0.8 ? "warning" : "info",
        message: `Executing step ${Math.floor(progress / 20) + 1}`,
        details: Math.random() > 0.7 ? "Additional details about this step execution" : undefined,
      }

      setLogs((prev) => [newLog, ...prev])

      // Add results
      if (progress % 20 === 0 && progress > 0) {
        const newResult: ExecutionResult = {
          id: `result-${Date.now()}`,
          stepName: ["Navigate to URL", "Click Login Button", "Enter Username", "Enter Password", "Submit Login Form"][
            Math.floor(progress / 20) - 1
          ],
          status: Math.random() > 0.9 ? "error" : "success",
          duration: Math.floor(Math.random() * 1000) + 100,
          message: Math.random() > 0.9 ? "Element not found" : undefined,
        }

        setResults((prev) => [...prev, newResult])
      }
    }, 1000)

    return () => clearInterval(interval)
  }

  const pauseExecution = () => {
    setIsPaused(true)
    toast({
      title: "Execution paused",
      description: "Workflow execution has been paused",
    })
    setStatusMessage("Execution paused ⏸️")
  }

  const stopExecution = () => {
    setIsRunning(false)
    setIsPaused(false)
    toast({
      title: "Execution stopped",
      description: "Workflow execution has been stopped",
    })
    setStatusMessage("Execution stopped 🛑")
  }

  const getLogIcon = (level: string) => {
    switch (level) {
      case "info":
        return (
          <div className="text-cyan-400">
            <AlertCircle className="h-4 w-4" />
          </div>
        )
      case "warning":
        return (
          <div className="text-amber-400">
            <AlertCircle className="h-4 w-4" />
          </div>
        )
      case "error":
        return (
          <div className="text-red-400">
            <XCircle className="h-4 w-4" />
          </div>
        )
      case "success":
        return (
          <div className="text-green-400">
            <CheckCircle2 className="h-4 w-4" />
          </div>
        )
      default:
        return (
          <div className="text-white/60">
            <AlertCircle className="h-4 w-4" />
          </div>
        )
    }
  }

  const getResultIcon = (status: string) => {
    switch (status) {
      case "success":
        return (
          <div className="text-green-400">
            <CheckCircle2 className="h-4 w-4" />
          </div>
        )
      case "error":
        return (
          <div className="text-red-400">
            <XCircle className="h-4 w-4" />
          </div>
        )
      case "skipped":
        return (
          <div className="text-white/60">
            <AlertCircle className="h-4 w-4" />
          </div>
        )
      default:
        return (
          <div className="text-white/60">
            <AlertCircle className="h-4 w-4" />
          </div>
        )
    }
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
              Execution Controls
            </h2>
            <TooltipProvider>
              <div className="flex gap-2">
                <Tooltip>
                  <TooltipTrigger asChild>
                    <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                      <Button
                        variant={isRunning && !isPaused ? "secondary" : "default"}
                        size="sm"
                        onClick={startExecution}
                        disabled={isRunning && !isPaused}
                        className={
                          isRunning && !isPaused
                            ? "bg-amber-500 text-white"
                            : isPaused
                              ? "bg-gradient-to-r from-amber-500 to-orange-500 text-white border-none shadow-lg shadow-amber-500/30"
                              : "bg-gradient-to-r from-green-500 to-emerald-500 text-white border-none shadow-lg shadow-green-500/30"
                        }
                      >
                        {countdown !== null ? (
                          <span className="font-bold">{countdown}</span>
                        ) : (
                          <>
                            <Play className="h-4 w-4 mr-1" /> {isPaused ? "Resume" : "Run"}
                          </>
                        )}
                      </Button>
                    </motion.div>
                  </TooltipTrigger>
                  <TooltipContent className="bg-black/80 backdrop-blur-xl border border-white/20 text-white">
                    <p>{isPaused ? "Resume execution" : "Run workflow"}</p>
                  </TooltipContent>
                </Tooltip>

                <Tooltip>
                  <TooltipTrigger asChild>
                    <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={pauseExecution}
                        disabled={!isRunning || isPaused}
                        className="bg-white/5 border border-white/20 text-white hover:bg-white/10"
                      >
                        <Pause className="h-4 w-4 mr-1" /> Pause
                      </Button>
                    </motion.div>
                  </TooltipTrigger>
                  <TooltipContent className="bg-black/80 backdrop-blur-xl border border-white/20 text-white">
                    <p>Pause execution</p>
                  </TooltipContent>
                </Tooltip>

                <Tooltip>
                  <TooltipTrigger asChild>
                    <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={stopExecution}
                        disabled={!isRunning}
                        className="bg-white/5 border border-white/20 text-white hover:bg-white/10"
                      >
                        <StopCircle className="h-4 w-4 mr-1" /> Stop
                      </Button>
                    </motion.div>
                  </TooltipTrigger>
                  <TooltipContent className="bg-black/80 backdrop-blur-xl border border-white/20 text-white">
                    <p>Stop execution</p>
                  </TooltipContent>
                </Tooltip>
              </div>
            </TooltipProvider>
          </div>

          <div className="space-y-4">
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <label htmlFor="workflow" className="text-white/80 text-sm font-medium">
                  Select Workflow
                </label>
                <Button
                  variant="ghost"
                  size="sm"
                  className="h-6 px-2 text-cyan-400 hover:text-cyan-300 hover:bg-white/5"
                >
                  <RefreshCw className="h-3 w-3 mr-1" /> Refresh
                </Button>
              </div>
              <Select value={selectedWorkflow} onValueChange={setSelectedWorkflow}>
                <SelectTrigger className="bg-white/5 border border-white/10 text-white focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500">
                  <SelectValue placeholder="Select a workflow" />
                </SelectTrigger>
                <SelectContent className="bg-black/80 backdrop-blur-xl border border-white/20 text-white">
                  <SelectItem value="login-workflow" className="focus:bg-white/10 focus:text-white">
                    Login Workflow
                  </SelectItem>
                  <SelectItem value="data-entry-workflow" className="focus:bg-white/10 focus:text-white">
                    Data Entry Workflow
                  </SelectItem>
                  <SelectItem value="checkout-workflow" className="focus:bg-white/10 focus:text-white">
                    Checkout Workflow
                  </SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div className="space-y-2">
              <label className="text-white/80 text-sm font-medium">Execution Progress</label>
              <div className="space-y-2">
                <div className="h-2 relative overflow-hidden rounded-full bg-white/10">
                  <motion.div
                    className="absolute top-0 left-0 h-full bg-gradient-to-r from-cyan-500 to-purple-500 rounded-full"
                    style={{ width: `${progress}%` }}
                    animate={
                      isRunning && !isPaused
                        ? {
                            boxShadow: [
                              "0 0 10px rgba(6, 182, 212, 0.5)",
                              "0 0 20px rgba(6, 182, 212, 0.5)",
                              "0 0 10px rgba(6, 182, 212, 0.5)",
                            ],
                          }
                        : {}
                    }
                    transition={{ repeat: Number.POSITIVE_INFINITY, duration: 1.5 }}
                  />
                </div>
                <div className="flex justify-between text-xs text-white/60">
                  <span>{progress}% Complete</span>
                  {isRunning && (
                    <span className={isPaused ? "text-amber-400" : "text-cyan-400"}>
                      {isPaused ? "Paused" : "Running..."}
                    </span>
                  )}
                </div>
              </div>
            </div>

            <div className="space-y-2">
              <label className="text-white/80 text-sm font-medium">Schedule Execution</label>
              <div className="grid grid-cols-2 gap-2">
                <motion.div whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
                  <Button
                    variant="outline"
                    size="sm"
                    className="justify-start w-full bg-white/5 border border-white/20 text-white hover:bg-white/10"
                  >
                    <Clock className="h-4 w-4 mr-2 text-cyan-400" /> Run at specific time
                  </Button>
                </motion.div>
                <motion.div whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
                  <Button
                    variant="outline"
                    size="sm"
                    className="justify-start w-full bg-white/5 border border-white/20 text-white hover:bg-white/10"
                  >
                    <Calendar className="h-4 w-4 mr-2 text-purple-400" /> Set recurring schedule
                  </Button>
                </motion.div>
              </div>
            </div>
          </div>

          <div className="flex-1">
            <Tabs defaultValue="results" className="flex-1 flex flex-col">
              <TabsList className="grid grid-cols-2 bg-white/5 border border-white/10 p-1">
                <TabsTrigger
                  value="results"
                  className="data-[state=active]:bg-gradient-to-r data-[state=active]:from-cyan-500 data-[state=active]:to-blue-500 data-[state=active]:text-white rounded-md"
                >
                  Results
                </TabsTrigger>
                <TabsTrigger
                  value="logs"
                  className="data-[state=active]:bg-gradient-to-r data-[state=active]:from-cyan-500 data-[state=active]:to-blue-500 data-[state=active]:text-white rounded-md"
                >
                  Logs
                </TabsTrigger>
              </TabsList>

              <div className="flex-1 mt-3">
                <TabsContent value="results" className="h-full">
                  <ScrollArea className="h-[calc(100%-1rem)] border border-white/10 rounded-lg bg-black/20">
                    <AnimatePresence>
                      <div className="p-3">
                        {results.length > 0 ? (
                          <div className="space-y-3">
                            {results.map((result, index) => (
                              <motion.div
                                key={result.id}
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: index * 0.1 }}
                                className={`p-3 rounded-lg border ${
                                  result.status === "error"
                                    ? "bg-red-500/10 border-red-500/30"
                                    : result.status === "success"
                                      ? "bg-green-500/10 border-green-500/30"
                                      : "bg-white/5 border-white/10"
                                }`}
                              >
                                <div className="flex items-start">
                                  <div className="mt-0.5 mr-2">{getResultIcon(result.status)}</div>
                                  <div className="flex-1">
                                    <div className="font-medium text-sm text-white">{result.stepName}</div>
                                    <div className="flex items-center justify-between text-xs">
                                      <span
                                        className={`capitalize ${
                                          result.status === "error"
                                            ? "text-red-400"
                                            : result.status === "success"
                                              ? "text-green-400"
                                              : "text-white/60"
                                        }`}
                                      >
                                        {result.status}
                                      </span>
                                      <span className="text-white/60">{result.duration}ms</span>
                                    </div>
                                    {result.message && (
                                      <div className="mt-1 text-xs text-white/80">{result.message}</div>
                                    )}
                                  </div>
                                </div>
                              </motion.div>
                            ))}
                          </div>
                        ) : (
                          <div className="p-6 text-center">
                            <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-white/10 flex items-center justify-center">
                              <Zap className="h-8 w-8 text-cyan-400" />
                            </div>
                            <p className="text-white/80">No results yet</p>
                            <p className="text-xs text-white/60 mt-1">Run a workflow to see results</p>
                          </div>
                        )}
                      </div>
                    </AnimatePresence>
                  </ScrollArea>
                </TabsContent>

                <TabsContent value="logs" className="h-full">
                  <ScrollArea className="h-[calc(100%-1rem)] border border-white/10 rounded-lg bg-black/20">
                    <AnimatePresence>
                      <div className="p-3">
                        {logs.length > 0 ? (
                          <div className="space-y-3">
                            {logs.map((log, index) => (
                              <motion.div
                                key={log.id}
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                transition={{ delay: index * 0.05 }}
                              >
                                <Accordion
                                  type="single"
                                  collapsible
                                  className="border border-white/10 rounded-lg bg-white/5"
                                >
                                  <AccordionItem value="item-1" className="border-none">
                                    <AccordionTrigger className="py-2 px-3 hover:no-underline">
                                      <div className="flex items-center gap-2 text-sm">
                                        <div>{getLogIcon(log.level)}</div>
                                        <div className="font-medium text-white">{log.message}</div>
                                        <Badge
                                          variant="outline"
                                          className={`ml-2 ${
                                            log.level === "error"
                                              ? "bg-red-500/10 text-red-400 border-red-500/30"
                                              : log.level === "warning"
                                                ? "bg-amber-500/10 text-amber-400 border-amber-500/30"
                                                : log.level === "success"
                                                  ? "bg-green-500/10 text-green-400 border-green-500/30"
                                                  : "bg-cyan-500/10 text-cyan-400 border-cyan-500/30"
                                          }`}
                                        >
                                          {log.level}
                                        </Badge>
                                        <div className="ml-auto text-xs text-white/60">
                                          {log.timestamp.toLocaleTimeString()}
                                        </div>
                                      </div>
                                    </AccordionTrigger>
                                    {log.details && (
                                      <AccordionContent className="px-3 pb-2 pt-0 text-xs">
                                        <div className="bg-black/30 p-3 rounded-md font-mono text-cyan-300 border border-white/10">
                                          {log.details}
                                        </div>
                                      </AccordionContent>
                                    )}
                                  </AccordionItem>
                                </Accordion>
                              </motion.div>
                            ))}
                          </div>
                        ) : (
                          <div className="p-6 text-center">
                            <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-white/10 flex items-center justify-center">
                              <Zap className="h-8 w-8 text-cyan-400" />
                            </div>
                            <p className="text-white/80">No logs yet</p>
                            <p className="text-xs text-white/60 mt-1">Run a workflow to see logs</p>
                          </div>
                        )}
                      </div>
                    </AnimatePresence>
                  </ScrollArea>
                </TabsContent>
              </div>
            </Tabs>
          </div>
        </CardContent>
      </Card>

      <Card className="flex flex-col bg-black/40 backdrop-blur-xl border border-white/10 shadow-xl rounded-xl overflow-hidden">
        <CardContent className="p-6 flex-1">
          <h2 className="text-xl font-bold bg-gradient-to-r from-cyan-400 to-purple-400 text-transparent bg-clip-text mb-4">
            Browser Preview
          </h2>
          <div className="border border-white/10 rounded-lg h-[calc(100%-2rem)] flex items-center justify-center bg-black/30 relative overflow-hidden">
            {isRunning && (
              <div className="absolute top-4 right-4 z-10">
                <div
                  className={`flex items-center gap-2 ${
                    isPaused ? "bg-amber-500" : "bg-green-500"
                  } text-white px-3 py-1.5 rounded-full text-sm font-medium ${
                    isPaused ? "" : "animate-pulse"
                  } shadow-lg ${isPaused ? "shadow-amber-500/30" : "shadow-green-500/30"}`}
                >
                  {isPaused ? <Pause className="h-3 w-3" /> : <RefreshCw className="h-3 w-3 animate-spin" />}
                  {isPaused ? "Paused" : "Executing Workflow"}
                </div>
              </div>
            )}

            {countdown !== null && (
              <motion.div
                initial={{ scale: 0.5, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                exit={{ scale: 2, opacity: 0 }}
                className="absolute inset-0 flex items-center justify-center bg-black/70 z-20"
              >
                <div className="text-8xl font-black text-white">{countdown}</div>
              </motion.div>
            )}

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
                <Flame className="h-12 w-12 text-white" />
              </motion.div>
              <p className="text-white/80 text-lg font-medium">
                {isRunning
                  ? isPaused
                    ? "Execution paused. Click 'Resume' to continue."
                    : "Executing workflow. Watch the progress in real-time."
                  : "Click 'Run' to execute the selected workflow"}
              </p>
              <p className="text-sm text-white/60 mt-2">The browser window will appear here during execution</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  )
}

