"use client"

import { Save, FolderOpen, Download, Settings, HelpCircle, FileText, Plus, Zap } from "lucide-react"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu"
import { Button } from "@/components/ui/button"
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from "@/components/ui/tooltip"
import { motion } from "framer-motion"

export function TopNavigation() {
  return (
    <motion.div
      initial={{ opacity: 0, y: -20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="border-b border-white/10 bg-black/30 backdrop-blur-xl sticky top-0 z-50"
    >
      <div className="container mx-auto flex items-center h-14 px-4">
        <TooltipProvider>
          <div className="flex space-x-1">
            {["File", "Edit", "View", "Help"].map((item, index) => (
              <DropdownMenu key={item}>
                <DropdownMenuTrigger asChild>
                  <motion.div whileHover={{ scale: 1.05 }} whileTap={{ scale: 0.95 }}>
                    <Button variant="ghost" size="sm" className="text-white/80 hover:text-white hover:bg-white/10">
                      {item}
                    </Button>
                  </motion.div>
                </DropdownMenuTrigger>
                <DropdownMenuContent className="bg-black/80 backdrop-blur-xl border border-white/20 text-white">
                  {item === "File" && (
                    <>
                      <DropdownMenuItem className="hover:bg-white/10 focus:bg-white/10">
                        <Plus className="mr-2 h-4 w-4 text-cyan-400" />
                        <span>New Workflow</span>
                      </DropdownMenuItem>
                      <DropdownMenuItem className="hover:bg-white/10 focus:bg-white/10">
                        <FolderOpen className="mr-2 h-4 w-4 text-yellow-400" />
                        <span>Open</span>
                      </DropdownMenuItem>
                      <DropdownMenuSeparator className="bg-white/20" />
                      <DropdownMenuItem className="hover:bg-white/10 focus:bg-white/10">
                        <Save className="mr-2 h-4 w-4 text-green-400" />
                        <span>Save</span>
                      </DropdownMenuItem>
                      <DropdownMenuItem className="hover:bg-white/10 focus:bg-white/10">
                        <FileText className="mr-2 h-4 w-4 text-blue-400" />
                        <span>Save As</span>
                      </DropdownMenuItem>
                      <DropdownMenuSeparator className="bg-white/20" />
                      <DropdownMenuItem className="hover:bg-white/10 focus:bg-white/10">
                        <Download className="mr-2 h-4 w-4 text-purple-400" />
                        <span>Export</span>
                      </DropdownMenuItem>
                    </>
                  )}
                  {item === "Edit" && (
                    <>
                      <DropdownMenuItem className="hover:bg-white/10 focus:bg-white/10">Undo</DropdownMenuItem>
                      <DropdownMenuItem className="hover:bg-white/10 focus:bg-white/10">Redo</DropdownMenuItem>
                      <DropdownMenuSeparator className="bg-white/20" />
                      <DropdownMenuItem className="hover:bg-white/10 focus:bg-white/10">Cut</DropdownMenuItem>
                      <DropdownMenuItem className="hover:bg-white/10 focus:bg-white/10">Copy</DropdownMenuItem>
                      <DropdownMenuItem className="hover:bg-white/10 focus:bg-white/10">Paste</DropdownMenuItem>
                    </>
                  )}
                  {item === "View" && (
                    <>
                      <DropdownMenuItem className="hover:bg-white/10 focus:bg-white/10">Zoom In</DropdownMenuItem>
                      <DropdownMenuItem className="hover:bg-white/10 focus:bg-white/10">Zoom Out</DropdownMenuItem>
                      <DropdownMenuItem className="hover:bg-white/10 focus:bg-white/10">Reset Zoom</DropdownMenuItem>
                    </>
                  )}
                  {item === "Help" && (
                    <>
                      <DropdownMenuItem className="hover:bg-white/10 focus:bg-white/10">Documentation</DropdownMenuItem>
                      <DropdownMenuItem className="hover:bg-white/10 focus:bg-white/10">
                        Keyboard Shortcuts
                      </DropdownMenuItem>
                      <DropdownMenuSeparator className="bg-white/20" />
                      <DropdownMenuItem className="hover:bg-white/10 focus:bg-white/10">
                        About AUTOCLICK
                      </DropdownMenuItem>
                    </>
                  )}
                </DropdownMenuContent>
              </DropdownMenu>
            ))}
          </div>

          <div className="ml-auto flex items-center space-x-2">
            <motion.div whileHover={{ scale: 1.1 }} whileTap={{ scale: 0.9 }} className="relative">
              <Button
                variant="ghost"
                size="icon"
                className="bg-gradient-to-r from-cyan-500 to-blue-500 text-white rounded-full shadow-lg shadow-cyan-500/30 border-none"
              >
                <Zap className="h-4 w-4" />
                <span className="sr-only">Power Actions</span>
              </Button>
              <div className="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full animate-pulse"></div>
            </motion.div>

            <motion.div whileHover={{ scale: 1.1 }} whileTap={{ scale: 0.9 }}>
              <Tooltip>
                <TooltipTrigger asChild>
                  <Button
                    variant="ghost"
                    size="icon"
                    className="bg-white/10 backdrop-blur-md border border-white/20 rounded-full text-white/80 hover:text-white"
                  >
                    <Settings className="h-4 w-4" />
                    <span className="sr-only">Settings</span>
                  </Button>
                </TooltipTrigger>
                <TooltipContent className="bg-black/80 backdrop-blur-xl border border-white/20 text-white">
                  <p>Settings</p>
                </TooltipContent>
              </Tooltip>
            </motion.div>

            <motion.div whileHover={{ scale: 1.1 }} whileTap={{ scale: 0.9 }}>
              <Tooltip>
                <TooltipTrigger asChild>
                  <Button
                    variant="ghost"
                    size="icon"
                    className="bg-white/10 backdrop-blur-md border border-white/20 rounded-full text-white/80 hover:text-white"
                  >
                    <HelpCircle className="h-4 w-4" />
                    <span className="sr-only">Help</span>
                  </Button>
                </TooltipTrigger>
                <TooltipContent className="bg-black/80 backdrop-blur-xl border border-white/20 text-white">
                  <p>Help</p>
                </TooltipContent>
              </Tooltip>
            </motion.div>
          </div>
        </TooltipProvider>
      </div>
    </motion.div>
  )
}

