"use client"

import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent } from "@/components/ui/card"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { Input } from "@/components/ui/input"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"
import { useToast } from "@/components/ui/use-toast"
import { executeWorkflow, getWorkflow, updateWorkflow, WorkflowStep } from "@/lib/api"
import { AnimatePresence, motion } from "framer-motion"
import { ArrowRight, Copy, FileText, Loader2, MoveDown, MoveUp, Play, Plus, Save, Settings, Trash2, Zap } from "lucide-react"
import { useEffect, useState } from "react"

export function WorkflowBuilderTab({ setStatusMessage }: { setStatusMessage: (message: string) => void }) {
  const [workflowName, setWorkflowName] = useState("New Workflow")
  const [workflowSteps, setWorkflowSteps] = useState<WorkflowStep[]>([])
  const [selectedStep, setSelectedStep] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)
  const [saving, setSaving] = useState(false)
  const [executing, setExecuting] = useState(false)
  const [workflowId, setWorkflowId] = useState("default") // Default workflow ID
  const { toast } = useToast()

  // Load workflow data when component mounts
  useEffect(() => {
    async function loadWorkflow() {
      try {
        setLoading(true)
        const data = await getWorkflow(workflowId)
        setWorkflowName(data.name)
        setWorkflowSteps(data.steps)
        setStatusMessage(`Workflow "${data.name}" loaded 📂`)
      } catch (error) {
        console.error("Failed to load workflow:", error)
        toast({
          title: "Error loading workflow",
          description: "Using default workflow instead",
          variant: "destructive"
        })
        // Set default workflow if API fails
        setWorkflowSteps([
          {
            id: "step1",
            type: "navigate",
            name: "Navigate to URL",
            target: "https://example.com",
            description: "Open the website homepage",
          },
          {
            id: "step2",
            type: "click",
            name: "Click Login Button",
            target: "button.login",
            description: "Click on the login button",
          },
          {
            id: "step3",
            type: "input",
            name: "Enter Username",
            target: "input#username",
            value: "user@example.com",
            description: "Enter the username in the input field",
          },
        ])
      } finally {
        setLoading(false)
      }
    }

    loadWorkflow()
  }, [workflowId, toast, setStatusMessage])

  const addStep = () => {
    const newStep: WorkflowStep = {
      id: `step${workflowSteps.length + 1}`,
      type: "click",
      name: "New Step",
      target: "",
      description: "Description of the step",
    }

    setWorkflowSteps([...workflowSteps, newStep])
    setSelectedStep(newStep.id)
    toast({
      title: "Step added",
      description: "New step added to workflow",
    })
  }

  const removeStep = (id: string) => {
    setWorkflowSteps(workflowSteps.filter((step) => step.id !== id))
    if (selectedStep === id) {
      setSelectedStep(null)
    }
    toast({
      title: "Step removed",
      description: "Step removed from workflow",
    })
  }

  const moveStep = (id: string, direction: "up" | "down") => {
    const index = workflowSteps.findIndex((step) => step.id === id)
    if ((direction === "up" && index === 0) || (direction === "down" && index === workflowSteps.length - 1)) {
      return
    }

    const newIndex = direction === "up" ? index - 1 : index + 1
    const newSteps = [...workflowSteps]
    const step = newSteps[index]
    newSteps.splice(index, 1)
    newSteps.splice(newIndex, 0, step)

    setWorkflowSteps(newSteps)
    toast({
      title: "Step moved",
      description: `Step moved ${direction}`,
    })
  }

  const duplicateStep = (id: string) => {
    const stepToDuplicate = workflowSteps.find((step) => step.id === id)
    if (!stepToDuplicate) return

    const newStep = {
      ...stepToDuplicate,
      id: `step${workflowSteps.length + 1}`,
      name: `${stepToDuplicate.name} (Copy)`,
    }

    const index = workflowSteps.findIndex((step) => step.id === id)
    const newSteps = [...workflowSteps]
    newSteps.splice(index + 1, 0, newStep)

    setWorkflowSteps(newSteps)
    setSelectedStep(newStep.id)
    toast({
      title: "Step duplicated",
      description: "Step has been duplicated",
    })
  }

  const saveWorkflow = async () => {
    try {
      setSaving(true)
      await updateWorkflow(workflowId, {
        name: workflowName,
        steps: workflowSteps
      })

      toast({
        title: "Workflow saved",
        description: `"${workflowName}" has been saved`,
      })
      setStatusMessage(`Workflow "${workflowName}" saved 💾`)
    } catch (error) {
      console.error("Failed to save workflow:", error)
      toast({
        title: "Error",
        description: "Failed to save workflow",
        variant: "destructive"
      })
    } finally {
      setSaving(false)
    }
  }

  const runWorkflow = async () => {
    try {
      setExecuting(true)
      const result = await executeWorkflow(workflowId)

      toast({
        title: "Workflow executed",
        description: result.message,
      })
      setStatusMessage(`Workflow execution: ${result.status} ✅`)
    } catch (error) {
      console.error("Failed to execute workflow:", error)
      toast({
        title: "Error",
        description: "Failed to execute workflow",
        variant: "destructive"
      })
    } finally {
      setExecuting(false)
    }
  }

  const getStepIcon = (type: string) => {
    switch (type) {
      case "navigate":
        return <ArrowRight className="h-4 w-4 text-cyan-400" />
      case "click":
        return <div className="w-4 h-4 flex items-center justify-center text-xs">🖱️</div>
      case "input":
        return <div className="w-4 h-4 flex items-center justify-center text-xs">⌨️</div>
      default:
        return <Settings className="h-4 w-4 text-purple-400" />
    }
  }

  const getStepColor = (type: string) => {
    switch (type) {
      case "navigate":
        return "from-cyan-500 to-blue-500 shadow-cyan-500/30"
      case "click":
        return "from-purple-500 to-pink-500 shadow-purple-500/30"
      case "input":
        return "from-green-500 to-emerald-500 shadow-green-500/30"
      default:
        return "from-amber-500 to-orange-500 shadow-amber-500/30"
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="h-full grid grid-cols-1 md:grid-cols-3 gap-6"
    >
      <Card className="md:col-span-1 flex flex-col bg-black/40 backdrop-blur-xl border border-white/10 shadow-xl rounded-xl overflow-hidden">
        <CardContent className="flex flex-col gap-4 p-6 flex-1">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-bold bg-gradient-to-r from-cyan-400 to-purple-400 text-transparent bg-clip-text">
              Steps
            </h2>
            <TooltipProvider>
              <div className="flex gap-2">
                <Tooltip>
                  <TooltipTrigger asChild>
                    <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={addStep}
                        className="bg-gradient-to-r from-green-500 to-emerald-500 text-white border-none shadow-lg shadow-green-500/30"
                      >
                        <Plus className="h-4 w-4 mr-1" /> Add
                      </Button>
                    </motion.div>
                  </TooltipTrigger>
                  <TooltipContent className="bg-black/80 backdrop-blur-xl border border-white/20 text-white">
                    <p>Add new step</p>
                  </TooltipContent>
                </Tooltip>
                <Tooltip>
                  <TooltipTrigger asChild>
                    <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={saveWorkflow}
                        disabled={saving}
                        className="bg-white/5 border border-white/20 text-white hover:bg-white/10"
                      >
                        {saving ? (
                          <>
                            <Loader2 className="h-4 w-4 mr-1 animate-spin" /> Saving...
                          </>
                        ) : (
                          <>
                            <Save className="h-4 w-4 mr-1" /> Save
                          </>
                        )}
                      </Button>
                    </motion.div>
                  </TooltipTrigger>
                  <TooltipContent className="bg-black/80 backdrop-blur-xl border border-white/20 text-white">
                    <p>Save workflow</p>
                  </TooltipContent>
                </Tooltip>
              </div>
            </TooltipProvider>
          </div>

          <div className="space-y-2">
            <label htmlFor="workflow-name" className="text-white/80 text-sm font-medium">
              Workflow Name
            </label>
            <Input
              id="workflow-name"
              value={workflowName}
              onChange={(e) => setWorkflowName(e.target.value)}
              className="h-9 bg-white/5 border border-white/10 text-white focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500"
            />
          </div>

          <ScrollArea className="flex-1 border border-white/10 rounded-lg bg-black/20">
            {loading ? (
              <div className="h-full flex items-center justify-center p-6">
                <div className="text-center">
                  <Loader2 className="h-8 w-8 mx-auto mb-4 animate-spin text-cyan-400" />
                  <p className="text-white/80">Loading workflow...</p>
                </div>
              </div>
            ) : (
              <AnimatePresence>
                <div className="p-2 space-y-2">
                {workflowSteps.map((step, index) => (
                  <motion.div
                    key={step.id}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.05 }}
                    className={`flex items-center p-3 rounded-lg cursor-pointer transition-all ${
                      selectedStep === step.id
                        ? "bg-white/10 border border-cyan-500/50 shadow-lg shadow-cyan-500/10"
                        : "hover:bg-white/5 border border-white/5"
                    }`}
                    onClick={() => setSelectedStep(step.id)}
                  >
                    <div className="flex items-center gap-3 flex-1 min-w-0">
                      <div
                        className={`flex items-center justify-center w-7 h-7 rounded-full bg-gradient-to-r ${getStepColor(step.type)} text-white shadow-sm`}
                      >
                        {index + 1}
                      </div>
                      <div className="flex-1 min-w-0">
                        <div className="font-medium text-sm truncate text-white">{step.name}</div>
                        <div className="flex items-center text-xs text-white/60">
                          {getStepIcon(step.type)}
                          <span className="ml-1 capitalize">{step.type}</span>
                        </div>
                      </div>
                    </div>
                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <Button
                          variant="ghost"
                          size="icon"
                          className="h-7 w-7 text-white/60 hover:text-white hover:bg-white/10 rounded-full"
                        >
                          <Settings className="h-3.5 w-3.5" />
                          <span className="sr-only">Actions</span>
                        </Button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent
                        align="end"
                        className="bg-black/80 backdrop-blur-xl border border-white/20 text-white"
                      >
                        <DropdownMenuItem
                          onClick={() => moveStep(step.id, "up")}
                          className="hover:bg-white/10 focus:bg-white/10"
                        >
                          <MoveUp className="h-4 w-4 mr-2 text-cyan-400" /> Move Up
                        </DropdownMenuItem>
                        <DropdownMenuItem
                          onClick={() => moveStep(step.id, "down")}
                          className="hover:bg-white/10 focus:bg-white/10"
                        >
                          <MoveDown className="h-4 w-4 mr-2 text-cyan-400" /> Move Down
                        </DropdownMenuItem>
                        <DropdownMenuItem
                          onClick={() => duplicateStep(step.id)}
                          className="hover:bg-white/10 focus:bg-white/10"
                        >
                          <Copy className="h-4 w-4 mr-2 text-purple-400" /> Duplicate
                        </DropdownMenuItem>
                        <DropdownMenuItem
                          onClick={() => removeStep(step.id)}
                          className="text-red-400 hover:bg-white/10 focus:bg-white/10"
                        >
                          <Trash2 className="h-4 w-4 mr-2" /> Delete
                        </DropdownMenuItem>
                      </DropdownMenuContent>
                    </DropdownMenu>
                  </motion.div>
                ))}
                {workflowSteps.length === 0 && (
                  <div className="p-6 text-center">
                    <div className="w-16 h-16 mx-auto mb-4 rounded-full bg-white/10 flex items-center justify-center">
                      <Zap className="h-8 w-8 text-cyan-400" />
                    </div>
                    <p className="text-white/80">No steps in workflow</p>
                    <p className="text-xs text-white/60 mt-1">Click "Add" to create a step</p>
                  </div>
                )}
                </div>
              </AnimatePresence>
            )}
          </ScrollArea>
        </CardContent>
      </Card>

      <Card className="md:col-span-2 flex flex-col bg-black/40 backdrop-blur-xl border border-white/10 shadow-xl rounded-xl overflow-hidden">
        <CardContent className="p-6 flex-1 flex flex-col">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-bold bg-gradient-to-r from-cyan-400 to-purple-400 text-transparent bg-clip-text">
              Workflow Diagram
            </h2>
            <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
              <Button
                variant="outline"
                size="sm"
                onClick={runWorkflow}
                disabled={executing}
                className="bg-gradient-to-r from-green-500 to-emerald-500 text-white border-none shadow-lg shadow-green-500/30"
              >
                {executing ? (
                  <>
                    <Loader2 className="h-4 w-4 mr-1 animate-spin" /> Running...
                  </>
                ) : (
                  <>
                    <Play className="h-4 w-4 mr-1" /> Test Workflow
                  </>
                )}
              </Button>
            </motion.div>
          </div>

          <div className="flex-1 border border-white/10 rounded-lg bg-black/20 overflow-auto p-6 relative">
            <div className="absolute inset-0 bg-[url('/grid.svg')] bg-center opacity-5"></div>

            {workflowSteps.length > 0 ? (
              <div className="flex flex-col items-center relative z-10">
                {workflowSteps.map((step, index) => (
                  <div key={step.id} className="flex flex-col items-center">
                    <motion.div
                      initial={{ opacity: 0, y: 20 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: index * 0.1 }}
                      className={`w-72 p-4 rounded-lg ${
                        selectedStep === step.id
                          ? "bg-gradient-to-r from-cyan-500/20 to-blue-500/20 border-2 border-cyan-500 shadow-lg shadow-cyan-500/20"
                          : "bg-black/40 backdrop-blur-sm border border-white/10"
                      }`}
                      whileHover={{ scale: 1.02 }}
                    >
                      <div className="flex items-center gap-3">
                        <Badge
                          variant="outline"
                          className={`h-7 w-7 p-0 flex items-center justify-center rounded-full bg-gradient-to-r ${getStepColor(step.type)} text-white border-none shadow-sm`}
                        >
                          {index + 1}
                        </Badge>
                        <div className="font-medium text-white">{step.name}</div>
                      </div>
                      <div className="mt-2 text-xs text-white/80">{step.description}</div>
                      {step.target && (
                        <div className="mt-2 text-xs">
                          <span className="text-white/60">Target: </span>
                          <code className="bg-white/10 px-1.5 py-0.5 rounded text-cyan-300">{step.target}</code>
                        </div>
                      )}
                      {step.value && (
                        <div className="mt-1 text-xs">
                          <span className="text-white/60">Value: </span>
                          <code className="bg-white/10 px-1.5 py-0.5 rounded text-purple-300">{step.value}</code>
                        </div>
                      )}
                    </motion.div>

                    {index < workflowSteps.length - 1 && (
                      <div className="h-10 w-px bg-gradient-to-b from-cyan-500 to-purple-500 relative">
                        <motion.div
                          className="absolute bottom-0 left-1/2 -translate-x-1/2 -translate-y-1/2 text-white"
                          animate={{ y: [0, 5, 0] }}
                          transition={{ repeat: Number.POSITIVE_INFINITY, duration: 1.5 }}
                        >
                          <ArrowRight className="h-5 w-5" />
                        </motion.div>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            ) : (
              <div className="h-full flex items-center justify-center">
                <div className="text-center">
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
                    <div className="w-24 h-24 mx-auto mb-6 rounded-full bg-gradient-to-r from-cyan-500 via-blue-500 to-purple-500 flex items-center justify-center shadow-xl shadow-blue-500/30">
                      <FileText className="h-12 w-12 text-white" />
                    </div>
                  </motion.div>
                  <p className="text-white/80 text-lg font-medium">Add steps to your workflow to see the diagram</p>
                  <p className="text-sm text-white/60 mt-2">Your automation flow will be visualized here</p>
                </div>
              </div>
            )}
          </div>
        </CardContent>
      </Card>
    </motion.div>
  )
}

