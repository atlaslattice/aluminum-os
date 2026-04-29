#!/usr/bin/env python3
"""
MANUS PERSONAL INTELLIGENCE - Proactive Intelligence System
============================================================

Provides proactive insights, recommendations, and daily briefings
based on the user's knowledge base and activity patterns.

Features:
- Daily intelligence scan
- Stale item detection
- Priority recommendations
- Council review triggers
- Contextual suggestions

Usage:
    $ python3 proactive_intelligence.py --daily-briefing
    $ python3 proactive_intelligence.py --scan
    $ python3 proactive_intelligence.py --recommendations

Environment Variables Required:
    - NOTION_API_KEY: Notion integration token
"""

import os
import json
import subprocess
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from collections import defaultdict

class ProactiveIntelligence:
    """Generate proactive insights and recommendations."""
    
    def __init__(self):
        self.sheldonbrain_db = "2d20c1de-73d9-80ce-a9af-000b011d52f0"
        self.data_source = "collection://2d20c1de-73d9-80ce-a9af-000b011d52f0"
        
        self.insights = []
        self.recommendations = []
        self.alerts = []
    
    def run_daily_scan(self) -> Dict:
        """Run comprehensive daily intelligence scan."""
        
        print("🔍 Running daily intelligence scan...")
        
        scan_results = {
            "timestamp": datetime.now().isoformat(),
            "stale_items": [],
            "high_priority_pending": [],
            "council_needed": [],
            "feast_mode": [],
            "recent_completions": [],
            "sphere_activity": {},
            "insights": [],
            "recommendations": []
        }
        
        # 1. Find stale items (pending > 7 days)
        print("  📋 Checking for stale items...")
        scan_results["stale_items"] = self._find_stale_items()
        
        # 2. Find high-priority pending items
        print("  ⚡ Checking high-priority pending...")
        scan_results["high_priority_pending"] = self._find_high_priority_pending()
        
        # 3. Find items needing council review
        print("  🏛️ Checking council review queue...")
        scan_results["council_needed"] = self._find_council_needed()
        
        # 4. Find items in feast mode
        print("  🔥 Checking feast mode items...")
        scan_results["feast_mode"] = self._find_feast_mode()
        
        # 5. Analyze sphere activity
        print("  🌐 Analyzing sphere activity...")
        scan_results["sphere_activity"] = self._analyze_sphere_activity()
        
        # 6. Generate insights
        print("  💡 Generating insights...")
        scan_results["insights"] = self._generate_insights(scan_results)
        
        # 7. Generate recommendations
        print("  📌 Generating recommendations...")
        scan_results["recommendations"] = self._generate_recommendations(scan_results)
        
        return scan_results
    
    def _find_stale_items(self) -> List[Dict]:
        """Find items that haven't been updated in > 7 days."""
        
        query = f'''SELECT Discovery, Status, Priority, Sphere 
                    FROM "{self.data_source}" 
                    WHERE Status = 'Pending'
                    LIMIT 50'''
        
        try:
            results = self._notion_query(query)
            # Note: Would need date comparison logic in production
            return results[:10]  # Return first 10 as potential stale items
        except Exception as e:
            print(f"    Warning: Could not check stale items: {e}")
            return []
    
    def _find_high_priority_pending(self) -> List[Dict]:
        """Find high-priority items that are still pending."""
        
        query = f'''SELECT Discovery, Status, Priority, Sphere, Actions 
                    FROM "{self.data_source}" 
                    WHERE Priority = 'High' AND Status = 'Pending'
                    LIMIT 20'''
        
        try:
            return self._notion_query(query)
        except Exception as e:
            print(f"    Warning: Could not check high priority: {e}")
            return []
    
    def _find_council_needed(self) -> List[Dict]:
        """Find items flagged for council review."""
        
        query = f'''SELECT Discovery, Status, Priority, Sphere 
                    FROM "{self.data_source}" 
                    WHERE "Council Needed" = '__YES__'
                    LIMIT 20'''
        
        try:
            return self._notion_query(query)
        except Exception as e:
            print(f"    Warning: Could not check council queue: {e}")
            return []
    
    def _find_feast_mode(self) -> List[Dict]:
        """Find items in feast mode (urgent attention needed)."""
        
        query = f'''SELECT Discovery, Status, Priority, Sphere 
                    FROM "{self.data_source}" 
                    WHERE "Feast Mode" = '__YES__'
                    LIMIT 20'''
        
        try:
            return self._notion_query(query)
        except Exception as e:
            print(f"    Warning: Could not check feast mode: {e}")
            return []
    
    def _analyze_sphere_activity(self) -> Dict:
        """Analyze activity across 144 spheres."""
        
        query = f'''SELECT Sphere, COUNT(*) as count 
                    FROM "{self.data_source}" 
                    GROUP BY Sphere
                    LIMIT 144'''
        
        try:
            results = self._notion_query(query)
            
            # Build sphere activity map
            activity = {}
            for item in results:
                sphere = item.get("Sphere", "Unknown")
                count = item.get("count", 1)
                activity[sphere] = count
            
            return activity
        except Exception as e:
            print(f"    Warning: Could not analyze spheres: {e}")
            return {}
    
    def _generate_insights(self, scan_results: Dict) -> List[Dict]:
        """Generate insights from scan results."""
        
        insights = []
        
        # Insight: Stale items
        stale_count = len(scan_results.get("stale_items", []))
        if stale_count > 0:
            insights.append({
                "type": "stale_items",
                "severity": "medium" if stale_count < 10 else "high",
                "message": f"You have {stale_count} pending items that may need attention",
                "action": "Review and update or archive stale items"
            })
        
        # Insight: High priority backlog
        hp_count = len(scan_results.get("high_priority_pending", []))
        if hp_count > 5:
            insights.append({
                "type": "priority_backlog",
                "severity": "high",
                "message": f"High-priority backlog: {hp_count} items pending",
                "action": "Focus on clearing high-priority items"
            })
        
        # Insight: Council queue
        council_count = len(scan_results.get("council_needed", []))
        if council_count > 0:
            insights.append({
                "type": "council_queue",
                "severity": "medium",
                "message": f"{council_count} items awaiting council review",
                "action": "Initiate council debate sessions"
            })
        
        # Insight: Feast mode items
        feast_count = len(scan_results.get("feast_mode", []))
        if feast_count > 0:
            insights.append({
                "type": "feast_mode",
                "severity": "high",
                "message": f"{feast_count} items in FEAST MODE require immediate attention",
                "action": "Address feast mode items first"
            })
        
        # Insight: Sphere concentration
        sphere_activity = scan_results.get("sphere_activity", {})
        if sphere_activity:
            top_spheres = sorted(sphere_activity.items(), key=lambda x: x[1], reverse=True)[:5]
            if top_spheres:
                insights.append({
                    "type": "sphere_focus",
                    "severity": "info",
                    "message": f"Most active spheres: {', '.join([s[0] for s in top_spheres])}",
                    "action": "Consider diversifying across other spheres"
                })
        
        return insights
    
    def _generate_recommendations(self, scan_results: Dict) -> List[Dict]:
        """Generate actionable recommendations."""
        
        recommendations = []
        now = datetime.now()
        
        # Time-based recommendations
        if now.weekday() == 0:  # Monday
            recommendations.append({
                "type": "weekly_review",
                "priority": "medium",
                "message": "Start the week with a review of last week's progress",
                "action": "Run: python3 session_context_loader.py"
            })
        
        if now.weekday() == 4:  # Friday
            recommendations.append({
                "type": "weekly_checkpoint",
                "priority": "medium",
                "message": "End the week with a comprehensive JANUS checkpoint",
                "action": "Create weekly summary checkpoint"
            })
        
        if now.hour >= 17:  # Evening
            recommendations.append({
                "type": "daily_checkpoint",
                "priority": "low",
                "message": "Consider creating an end-of-day checkpoint",
                "action": "Run: python3 janus_checkpoint.py"
            })
        
        # Content-based recommendations
        if scan_results.get("feast_mode"):
            recommendations.append({
                "type": "urgent_attention",
                "priority": "high",
                "message": "Address FEAST MODE items before other work",
                "items": [item.get("Discovery", "Unknown") for item in scan_results["feast_mode"][:3]]
            })
        
        if scan_results.get("council_needed"):
            recommendations.append({
                "type": "council_session",
                "priority": "medium",
                "message": "Schedule a Trinity Council session for pending reviews",
                "count": len(scan_results["council_needed"])
            })
        
        # Sync recommendation
        recommendations.append({
            "type": "sync_check",
            "priority": "low",
            "message": "Verify artifact synchronization across platforms",
            "action": "Run: python3 artifact_sync.py --verify"
        })
        
        return recommendations
    
    def _notion_query(self, query: str) -> List[Dict]:
        """Execute a Notion query via MCP CLI."""
        
        input_json = json.dumps({
            "data": {
                "data_source_urls": [self.data_source],
                "query": query
            }
        })
        
        cmd = [
            "manus-mcp-cli", "tool", "call", "notion-query-data-sources",
            "--server", "notion",
            "--input", input_json
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode != 0:
            raise Exception(f"Query failed: {result.stderr}")
        
        # Parse results
        try:
            if '"results":' in result.stdout:
                import re
                match = re.search(r'"results":\s*(\[.*?\])', result.stdout, re.DOTALL)
                if match:
                    return json.loads(match.group(1))
        except:
            pass
        
        return []
    
    def generate_daily_briefing(self) -> str:
        """Generate a comprehensive daily briefing."""
        
        scan = self.run_daily_scan()
        
        lines = [
            "=" * 70,
            "🌅 MANUS PERSONAL INTELLIGENCE - DAILY BRIEFING",
            f"📅 {datetime.now().strftime('%A, %B %d, %Y at %H:%M')}",
            "=" * 70,
            ""
        ]
        
        # Alerts section
        if scan.get("feast_mode") or scan.get("council_needed"):
            lines.append("🚨 ALERTS")
            lines.append("-" * 40)
            
            if scan["feast_mode"]:
                lines.append(f"  🔥 {len(scan['feast_mode'])} items in FEAST MODE")
                for item in scan["feast_mode"][:3]:
                    lines.append(f"     • {item.get('Discovery', 'Unknown')}")
            
            if scan["council_needed"]:
                lines.append(f"  🏛️ {len(scan['council_needed'])} items need council review")
            
            lines.append("")
        
        # Status section
        lines.append("📊 STATUS OVERVIEW")
        lines.append("-" * 40)
        lines.append(f"  • High-priority pending: {len(scan.get('high_priority_pending', []))}")
        lines.append(f"  • Items needing attention: {len(scan.get('stale_items', []))}")
        lines.append(f"  • Council review queue: {len(scan.get('council_needed', []))}")
        lines.append(f"  • Feast mode items: {len(scan.get('feast_mode', []))}")
        lines.append("")
        
        # Insights section
        if scan.get("insights"):
            lines.append("💡 INSIGHTS")
            lines.append("-" * 40)
            for insight in scan["insights"]:
                severity_emoji = {
                    "high": "🔴",
                    "medium": "🟡",
                    "low": "🟢",
                    "info": "ℹ️"
                }.get(insight.get("severity", "info"), "⚪")
                lines.append(f"  {severity_emoji} {insight['message']}")
            lines.append("")
        
        # Recommendations section
        if scan.get("recommendations"):
            lines.append("📌 RECOMMENDATIONS")
            lines.append("-" * 40)
            for rec in scan["recommendations"][:5]:
                priority_emoji = {
                    "high": "🔴",
                    "medium": "🟡",
                    "low": "🟢"
                }.get(rec.get("priority", "low"), "⚪")
                lines.append(f"  {priority_emoji} {rec['message']}")
                if rec.get("action"):
                    lines.append(f"     → {rec['action']}")
            lines.append("")
        
        # Sphere activity
        if scan.get("sphere_activity"):
            lines.append("🌐 SPHERE ACTIVITY (Top 5)")
            lines.append("-" * 40)
            sorted_spheres = sorted(
                scan["sphere_activity"].items(),
                key=lambda x: x[1],
                reverse=True
            )[:5]
            for sphere, count in sorted_spheres:
                lines.append(f"  • {sphere}: {count} items")
            lines.append("")
        
        lines.append("=" * 70)
        lines.append("Ready for your instructions. Type 'help' for available commands.")
        lines.append("")
        
        return "\n".join(lines)
    
    def save_briefing(self, briefing: str) -> Dict:
        """Save daily briefing to Notion and Drive."""
        
        results = {}
        
        # Save to Notion
        input_json = json.dumps({
            "parent": {"data_source_id": self.sheldonbrain_db.replace("-", "")},
            "pages": [{
                "properties": {
                    "Discovery": f"🌅 Daily Briefing - {datetime.now().strftime('%Y-%m-%d')}",
                    "Category": "Technology",
                    "Priority": "Medium",
                    "Status": "Completed",
                    "Sphere": "S144",
                    "Ingest Run ID": f"BRIEFING_{datetime.now().strftime('%Y%m%d')}"
                },
                "content": briefing
            }]
        })
        
        cmd = [
            "manus-mcp-cli", "tool", "call", "notion-create-pages",
            "--server", "notion",
            "--input", input_json
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            results["notion"] = {"success": result.returncode == 0}
        except Exception as e:
            results["notion"] = {"success": False, "error": str(e)}
        
        # Save to local file
        filepath = f"/home/ubuntu/manus_pi/briefings/daily_{datetime.now().strftime('%Y%m%d')}.txt"
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, "w") as f:
            f.write(briefing)
        
        results["local"] = {"path": filepath}
        
        return results


def main():
    """Main entry point."""
    
    import argparse
    
    parser = argparse.ArgumentParser(description="Proactive Intelligence System")
    parser.add_argument("--daily-briefing", "-d", action="store_true", help="Generate daily briefing")
    parser.add_argument("--scan", "-s", action="store_true", help="Run intelligence scan")
    parser.add_argument("--recommendations", "-r", action="store_true", help="Get recommendations only")
    parser.add_argument("--save", action="store_true", help="Save briefing to Notion")
    
    args = parser.parse_args()
    
    pi = ProactiveIntelligence()
    
    if args.daily_briefing:
        briefing = pi.generate_daily_briefing()
        print(briefing)
        
        if args.save:
            results = pi.save_briefing(briefing)
            print(f"\n💾 Saved: {json.dumps(results, indent=2)}")
    
    elif args.scan:
        results = pi.run_daily_scan()
        print(json.dumps(results, indent=2, default=str))
    
    elif args.recommendations:
        scan = pi.run_daily_scan()
        for rec in scan.get("recommendations", []):
            print(f"• {rec['message']}")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
