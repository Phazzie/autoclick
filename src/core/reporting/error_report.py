"""
Error report for analyzing system errors.
"""
from typing import Any, Dict, List, Optional, Counter
from datetime import datetime
from collections import defaultdict

from src.core.reporting.base_report import BaseReport
from src.core.errors.error_types import Error, ErrorType, ErrorSeverity


class ErrorReport(BaseReport):
    """
    Report for system error analysis.
    
    This report provides detailed information about system errors,
    including error types, frequencies, and patterns.
    """
    
    def __init__(
        self,
        title: str = "Error Analysis Report",
        description: Optional[str] = None,
        tags: Optional[List[str]] = None
    ):
        """
        Initialize the error report.
        
        Args:
            title: Report title
            description: Optional report description
            tags: Optional list of tags for categorization
        """
        super().__init__(
            report_type="error",
            title=title,
            description=description,
            tags=tags
        )
        self.data = {
            "errors": [],
            "error_types": {},
            "error_sources": {},
            "error_severity": {},
            "patterns": [],
            "summary": {
                "total_errors": 0,
                "critical_errors": 0,
                "error_rate": 0,
                "most_common_type": None,
                "most_common_source": None
            }
        }
        
    def collect_data(self, errors: List[Error]) -> None:
        """
        Collect error data.
        
        Args:
            errors: List of errors to analyze
        """
        self.source = errors
        self.data["collection_time"] = datetime.now().isoformat()
        
        # Store errors
        self.data["errors"] = [error.to_dict() for error in errors]
        
        # Analyze errors
        self._analyze_errors(errors)
        
    def _analyze_errors(self, errors: List[Error]) -> None:
        """
        Analyze errors.
        
        Args:
            errors: List of errors to analyze
        """
        # Skip analysis if no errors
        if not errors:
            self.logger.warning("No errors found for analysis")
            return
            
        # Analyze error types
        self._analyze_error_types(errors)
        
        # Analyze error sources
        self._analyze_error_sources(errors)
        
        # Analyze error severity
        self._analyze_error_severity(errors)
        
        # Identify patterns
        self._identify_patterns(errors)
        
        # Create summary
        self._create_summary(errors)
        
    def _analyze_error_types(self, errors: List[Error]) -> None:
        """
        Analyze error types.
        
        Args:
            errors: List of errors to analyze
        """
        # Count error types
        type_counter = Counter(error.error_type for error in errors)
        
        # Create error type statistics
        error_types = {}
        for error_type, count in type_counter.items():
            error_types[error_type.name] = {
                "count": count,
                "percentage": (count / len(errors)) * 100,
                "examples": [
                    error.to_dict() for error in errors[:3] 
                    if error.error_type == error_type
                ]
            }
            
        self.data["error_types"] = error_types
        
    def _analyze_error_sources(self, errors: List[Error]) -> None:
        """
        Analyze error sources.
        
        Args:
            errors: List of errors to analyze
        """
        # Group errors by source
        sources = defaultdict(list)
        for error in errors:
            source = error.source or "unknown"
            sources[source].append(error)
            
        # Create source statistics
        error_sources = {}
        for source, source_errors in sources.items():
            error_sources[source] = {
                "count": len(source_errors),
                "percentage": (len(source_errors) / len(errors)) * 100,
                "types": Counter(error.error_type.name for error in source_errors),
                "examples": [error.to_dict() for error in source_errors[:3]]
            }
            
        self.data["error_sources"] = error_sources
        
    def _analyze_error_severity(self, errors: List[Error]) -> None:
        """
        Analyze error severity.
        
        Args:
            errors: List of errors to analyze
        """
        # Group errors by severity
        severity_groups = defaultdict(list)
        for error in errors:
            severity_groups[error.severity].append(error)
            
        # Create severity statistics
        error_severity = {}
        for severity, severity_errors in severity_groups.items():
            error_severity[severity.name] = {
                "count": len(severity_errors),
                "percentage": (len(severity_errors) / len(errors)) * 100,
                "types": Counter(error.error_type.name for error in severity_errors),
                "examples": [error.to_dict() for error in severity_errors[:3]]
            }
            
        self.data["error_severity"] = error_severity
        
    def _identify_patterns(self, errors: List[Error]) -> None:
        """
        Identify error patterns.
        
        Args:
            errors: List of errors to analyze
        """
        patterns = []
        
        # Look for temporal patterns (errors occurring close together)
        if len(errors) >= 3:
            # Sort errors by timestamp
            sorted_errors = sorted(errors, key=lambda e: e.timestamp)
            
            # Look for clusters of errors
            clusters = self._find_error_clusters(sorted_errors)
            
            for cluster in clusters:
                if len(cluster) >= 3:
                    # Check if cluster has a dominant error type
                    type_counter = Counter(error.error_type for error in cluster)
                    most_common_type, type_count = type_counter.most_common(1)[0]
                    
                    if type_count >= len(cluster) * 0.7:  # 70% of cluster is same type
                        patterns.append({
                            "type": "temporal_cluster",
                            "error_type": most_common_type.name,
                            "count": len(cluster),
                            "start_time": min(error.timestamp for error in cluster).isoformat(),
                            "end_time": max(error.timestamp for error in cluster).isoformat(),
                            "examples": [error.to_dict() for error in cluster[:3]]
                        })
                        
        # Look for source patterns (multiple error types from same source)
        source_errors = defaultdict(list)
        for error in errors:
            if error.source:
                source_errors[error.source].append(error)
                
        for source, source_error_list in source_errors.items():
            if len(source_error_list) >= 3:
                type_counter = Counter(error.error_type for error in source_error_list)
                
                if len(type_counter) >= 3:  # At least 3 different error types
                    patterns.append({
                        "type": "source_pattern",
                        "source": source,
                        "error_types": [t.name for t in type_counter.keys()],
                        "count": len(source_error_list),
                        "examples": [error.to_dict() for error in source_error_list[:3]]
                    })
                    
        self.data["patterns"] = patterns
        
    def _find_error_clusters(self, sorted_errors: List[Error], max_gap_seconds: int = 60) -> List[List[Error]]:
        """
        Find clusters of errors occurring close together in time.
        
        Args:
            sorted_errors: List of errors sorted by timestamp
            max_gap_seconds: Maximum gap between errors in a cluster (seconds)
            
        Returns:
            List of error clusters
        """
        if not sorted_errors:
            return []
            
        clusters = []
        current_cluster = [sorted_errors[0]]
        
        for i in range(1, len(sorted_errors)):
            current_error = sorted_errors[i]
            previous_error = sorted_errors[i-1]
            
            # Calculate time difference in seconds
            time_diff = (current_error.timestamp - previous_error.timestamp).total_seconds()
            
            if time_diff <= max_gap_seconds:
                # Add to current cluster
                current_cluster.append(current_error)
            else:
                # Start a new cluster
                if len(current_cluster) >= 2:
                    clusters.append(current_cluster)
                current_cluster = [current_error]
                
        # Add the last cluster if it has at least 2 errors
        if len(current_cluster) >= 2:
            clusters.append(current_cluster)
            
        return clusters
        
    def _create_summary(self, errors: List[Error]) -> None:
        """
        Create a summary of all errors.
        
        Args:
            errors: List of errors to analyze
        """
        if not errors:
            return
            
        # Count critical errors
        critical_errors = sum(
            1 for error in errors 
            if error.severity in (ErrorSeverity.CRITICAL, ErrorSeverity.FATAL)
        )
        
        # Find most common error type
        type_counter = Counter(error.error_type.name for error in errors)
        most_common_type = type_counter.most_common(1)[0][0] if type_counter else None
        
        # Find most common source
        source_counter = Counter(error.source for error in errors if error.source)
        most_common_source = source_counter.most_common(1)[0][0] if source_counter else None
        
        # Update summary
        self.data["summary"] = {
            "total_errors": len(errors),
            "critical_errors": critical_errors,
            "error_rate": critical_errors / len(errors) if errors else 0,
            "most_common_type": most_common_type,
            "most_common_source": most_common_source
        }
        
    def get_error_types(self) -> Dict[str, Dict[str, Any]]:
        """
        Get error type statistics.
        
        Returns:
            Dictionary mapping error types to statistics
        """
        return self.data["error_types"]
        
    def get_error_sources(self) -> Dict[str, Dict[str, Any]]:
        """
        Get error source statistics.
        
        Returns:
            Dictionary mapping error sources to statistics
        """
        return self.data["error_sources"]
        
    def get_error_patterns(self) -> List[Dict[str, Any]]:
        """
        Get identified error patterns.
        
        Returns:
            List of error patterns
        """
        return self.data["patterns"]
        
    def get_critical_errors(self) -> List[Dict[str, Any]]:
        """
        Get critical and fatal errors.
        
        Returns:
            List of critical and fatal errors
        """
        return [
            error for error in self.data["errors"]
            if error["severity"] in ("CRITICAL", "FATAL")
        ]
        
    def get_errors_by_type(self, error_type: str) -> List[Dict[str, Any]]:
        """
        Get errors of a specific type.
        
        Args:
            error_type: Error type name
            
        Returns:
            List of errors of the specified type
        """
        return [
            error for error in self.data["errors"]
            if error["type"] == error_type
        ]
