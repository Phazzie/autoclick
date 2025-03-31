"use client"

import { useState, useEffect } from "react"
import { Play, Square, Save, Zap, Flame } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { useToast } from "@/components/ui/use-toast"
import { motion, AnimatePresence } from "framer-motion"

type RecordedAction = {
  id: number
  type: string
  target: string
  value?: string
  timestamp: Date
}

export function RecordTab({ setStatusMessage }: { setStatusMessage: (message: string) => void }) {
  const [isRecording, setIsRecording] = useState(false)
  const [recordedActions, setRecordedActions] = useState<RecordedAction[]>([])
  const [sessionName, setSessionName] = useState("")
  const { toast } = useToast()
  const [countdown, setCountdown] = useState<number | null>(null)

  useEffect(() => {
    if (countdown !== null && countdown > 0) {
      const timer = setTimeout(() => setCountdown(countdown - 1), 1000)
      return () => clearTimeout(timer)
    } else if (countdown === 0) {
      setCountdown(null)
      startActualRecording()
    }
  }, [countdown])

  const toggleRecording = () => {
    if (isRecording) {
      setIsRecording(false)
      setStatusMessage("Recording stopped! 🛑")
      toast({
        title: "Recording stopped",
        description: `Captured ${recordedActions.length} actions`,
        variant: "default",
      })
    } else {
      setCountdown(3)
      setStatusMessage("Get ready to record! 🎬")
      toast({
        title: "Recording starting in 3...",
        description: "Prepare your browser actions",
        variant: "default",
      })
    }
  }

  const startActualRecording = () => {
    setIsRecording(true)
    setStatusMessage("Recording in progress... 🔴")
    toast({
      title: "Recording started",
      description: "Capturing browser actions",
      variant: "default",
    })

    // Simulate recording some actions
    const demoActions: RecordedAction[] = [
      { id: 1, type: "click", target: "button.login", timestamp: new Date() },
      { id: 2, type: "input", target: "input#username", value: "user@example.com", timestamp: new Date() },
      { id: 3, type: "input", target: "input#password", value: "********", timestamp: new Date() },
      { id: 4, type: "click", target: "button[type='submit']", timestamp: new Date() },
    ]

    setTimeout(() => {
      setRecordedActions(demoActions)
    }, 2000)
  }

  const saveSession = () => {
    if (sessionName.trim() === "") {
      toast({
        title: "Error",
        description: "Please enter a session name",
        variant: "destructive",
      })
      return
    }

    toast({
      title: "Session saved",
      description: `Saved ${recordedActions.length} actions as "${sessionName}"`,
      variant: "default",
    })
    setStatusMessage(`Session "${sessionName}" saved 💾`)
  }

  const getActionIcon = (type: string) => {
    switch (type) {
      case "click":
        return <div className="w-5 h-5 flex items-center justify-center text-base">🖱️</div>
      case "input":
        return <div className="w-5 h-5 flex items-center justify-center text-base">⌨️</div>
      default:
        return <div className="w-5 h-5 flex items-center justify-center text-base">🔍</div>
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
              Recording Controls
            </h2>
            <TooltipProvider>
              <div className="flex gap-2">
                <Tooltip>
                  <TooltipTrigger asChild>
                    <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                      <Button
                        variant={isRecording ? "destructive" : "default"}
                        size="sm"
                        onClick={toggleRecording}
                        className={
                          isRecording
                            ? "bg-gradient-to-r from-red-500 to-pink-500 text-white border-none shadow-lg shadow-red-500/30"
                            : "bg-gradient-to-r from-green-500 to-emerald-500 text-white border-none shadow-lg shadow-green-500/30"
                        }
                      >
                        {countdown !== null ? (
                          <span className="font-bold">{countdown}</span>
                        ) : isRecording ? (
                          <>
                            <Square className="h-4 w-4 mr-2" /> Stop
                          </>
                        ) : (
                          <>
                            <Play className="h-4 w-4 mr-2" /> Start
                          </>
                        )}
                      </Button>
                    </motion.div>
                  </TooltipTrigger>
                  <TooltipContent className="bg-black/80 backdrop-blur-xl border border-white/20 text-white">
                    <p>{isRecording ? "Stop recording" : "Start recording"}</p>
                  </TooltipContent>
                </Tooltip>

                <Tooltip>
                  <TooltipTrigger asChild>
                    <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={saveSession}
                        disabled={recordedActions.length === 0}
                        className="bg-white/5 border border-white/20 text-white hover:bg-white/10"
                      >
                        <Save className="h-4 w-4 mr-2" /> Save
                      </Button>
                    </motion.div>
                  </TooltipTrigger>
                  <TooltipContent className="bg-black/80 backdrop-blur-xl border border-white/20 text-white">
                    <p>Save recording session</p>
                  </TooltipContent>
                </Tooltip>
              </div>
            </TooltipProvider>
          </div>

          <div className="space-y-2">
            <Label htmlFor="session-name" className="text-white/80">
              Session Name
            </Label>
            <Input
              id="session-name"
              placeholder="Enter session name"
              value={sessionName}
              onChange={(e) => setSessionName(e.target.value)}
              className="bg-white/5 border border-white/10 text-white focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500"
            />
          </div>

          <div className="flex-1">
            <h3 className="text-sm font-medium mb-2 text-white/80">Recorded Actions</h3>
            <ScrollArea className="h-[calc(100%-2rem)] border border-white/10 rounded-lg bg-black/20">
              <AnimatePresence>
                {recordedActions.length > 0 ? (
                  <ul className="p-4 space-y-3">
                    {recordedActions.map((action, index) => (
                      <motion.li
                        key={action.id}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: index * 0.1 }}
                        className="p-3 bg-white/5 hover:bg-white/10 transition-colors rounded-lg text-sm border border-white/10"
                      >
                        <div className="flex justify-between">
                          <div className="flex items-center">
                            {getActionIcon(action.type)}
                            <span className="font-medium capitalize ml-2 text-white">{action.type}</span>
                          </div>
                          <span className="text-xs text-white/60">{action.timestamp.toLocaleTimeString()}</span>
                        </div>
                        <div className="text-xs mt-2">
                          <span className="text-white/60">Target: </span>
                          <code className="bg-white/10 px-1 py-0.5 rounded text-cyan-300">{action.target}</code>
                        </div>
                        {action.value && (
                          <div className="text-xs mt-1">
                            <span className="text-white/60">Value: </span>
                            <code className="bg-white/10 px-1 py-0.5 rounded text-purple-300">{action.value}</code>
                          </div>
                        )}
                      </motion.li>
                    ))}
                  </ul>
                ) : (
                  <div className="p-8 text-center">
                    {isRecording ? (
                      <motion.div
                        animate={{ scale: [1, 1.05, 1] }}
                        transition={{ repeat: Number.POSITIVE_INFINITY, duration: 2 }}
                      >
                        <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-gradient-to-r from-red-500 to-pink-500 flex items-center justify-center shadow-lg shadow-red-500/30 animate-pulse">
                          <Flame className="h-8 w-8 text-white" />
                        </div>
                        <p className="text-white/80">Recording in progress...</p>
                        <p className="text-xs text-white/60 mt-1">Actions will appear here</p>
                      </motion.div>
                    ) : (
                      <motion.div>
                        <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-white/10 flex items-center justify-center">
                          <Zap className="h-8 w-8 text-cyan-400" />
                        </div>
                        <p className="text-white/80">No actions recorded yet</p>
                        <p className="text-xs text-white/60 mt-1">Click 'Start' to begin recording</p>
                      </motion.div>
                    )}
                  </div>
                )}
              </AnimatePresence>
            </ScrollArea>
          </div>
        </CardContent>
      </Card>

      <Card className="flex flex-col bg-black/40 backdrop-blur-xl border border-white/10 shadow-xl rounded-xl overflow-hidden">
        <CardContent className="p-6 flex-1">
          <h2 className="text-xl font-bold bg-gradient-to-r from-cyan-400 to-purple-400 text-transparent bg-clip-text mb-4">
            Browser Preview
          </h2>
          <div className="border border-white/10 rounded-lg h-[calc(100%-2rem)] flex items-center justify-center bg-black/30 relative overflow-hidden">
            {isRecording && (
              <div className="absolute top-4 right-4 z-10">
                <div className="flex items-center gap-2 bg-red-500 text-white px-3 py-1.5 rounded-full text-sm font-medium animate-pulse shadow-lg shadow-red-500/30">
                  <div className="w-3 h-3 rounded-full bg-white"></div>
                  REC
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
                <Play className="h-12 w-12 text-white" />
              </motion.div>
              <p className="text-white/80 text-lg font-medium">
                {isRecording ? "Capturing your browser actions..." : "Click 'Start' to begin recording browser actions"}
              </p>
              <p className="text-sm text-white/60 mt-2">The browser window will appear here when connected</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </motion.div>
  )
}

