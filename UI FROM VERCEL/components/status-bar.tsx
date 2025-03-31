"use client"

import { motion } from "framer-motion"
import { Cpu } from "lucide-react"

export function StatusBar({ message }: { message: string }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.2 }}
      className="h-8 border-t border-white/10 bg-black/30 backdrop-blur-xl px-4 py-1 flex items-center"
    >
      <div className="flex items-center">
        <Cpu className="h-3 w-3 mr-2 text-cyan-400" />
        <div className="text-xs text-cyan-300 font-medium">{message}</div>
      </div>
      <div className="ml-auto flex items-center space-x-3">
        <div className="flex items-center">
          <div className="w-2 h-2 rounded-full bg-green-500 mr-2 animate-pulse"></div>
          <span className="text-xs text-white/60">Connected</span>
        </div>
        <div className="text-xs text-white/60">v2.0.4</div>
      </div>
    </motion.div>
  )
}

