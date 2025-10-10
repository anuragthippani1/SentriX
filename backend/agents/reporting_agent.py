import json
import uuid
from datetime import datetime
from typing import List, Dict, Any
from models.schemas import RiskReport, PoliticalRisk, ScheduleRisk
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
import os

class ReportingAgent:
    def __init__(self):
        self.reports_dir = "reports"
        if not os.path.exists(self.reports_dir):
            os.makedirs(self.reports_dir)
    
    async def generate_political_report(self, political_risks: List[PoliticalRisk], session_id: str) -> RiskReport:
        """Generate a political risk report"""
        report_id = str(uuid.uuid4())
        
        # Generate executive summary
        executive_summary = self._generate_political_summary(political_risks)
        
        # Generate recommendations
        recommendations = self._generate_political_recommendations(political_risks)
        
        # Create world risk data for visualization
        world_risk_data = self._create_world_risk_data(political_risks)
        
        report = RiskReport(
            report_id=report_id,
            session_id=session_id,
            report_type="political",
            created_at=datetime.now(),
            title="Political Risk Assessment Report",
            executive_summary=executive_summary,
            political_risks=political_risks,
            world_risk_data=world_risk_data,
            recommendations=recommendations
        )
        
        return report
    
    async def generate_schedule_report(self, schedule_risks: List[ScheduleRisk], session_id: str) -> RiskReport:
        """Generate a schedule risk report"""
        report_id = str(uuid.uuid4())
        
        # Generate executive summary
        executive_summary = self._generate_schedule_summary(schedule_risks)
        
        # Generate recommendations
        recommendations = self._generate_schedule_recommendations(schedule_risks)
        
        report = RiskReport(
            report_id=report_id,
            session_id=session_id,
            report_type="schedule",
            created_at=datetime.now(),
            title="Schedule Risk Assessment Report",
            executive_summary=executive_summary,
            schedule_risks=schedule_risks,
            recommendations=recommendations
        )
        
        return report
    
    async def generate_combined_report(self, political_risks: List[PoliticalRisk], 
                                     schedule_risks: List[ScheduleRisk], session_id: str) -> RiskReport:
        """Generate a combined risk report"""
        report_id = str(uuid.uuid4())
        
        # Generate executive summary
        executive_summary = self._generate_combined_summary(political_risks, schedule_risks)
        
        # Generate recommendations
        recommendations = self._generate_combined_recommendations(political_risks, schedule_risks)
        
        # Create world risk data
        world_risk_data = self._create_combined_world_risk_data(political_risks, schedule_risks)
        
        report = RiskReport(
            report_id=report_id,
            session_id=session_id,
            report_type="combined",
            created_at=datetime.now(),
            title="Comprehensive Risk Assessment Report",
            executive_summary=executive_summary,
            political_risks=political_risks,
            schedule_risks=schedule_risks,
            world_risk_data=world_risk_data,
            recommendations=recommendations
        )
        
        return report
    
    def _generate_political_summary(self, political_risks: List[PoliticalRisk]) -> str:
        """Generate executive summary for political risks"""
        if not political_risks:
            return "No significant political risks identified in the analyzed countries."
        
        high_risk_countries = [risk for risk in political_risks if risk.likelihood_score >= 4]
        medium_risk_countries = [risk for risk in political_risks if risk.likelihood_score == 3]
        
        summary = f"Political risk analysis identified {len(political_risks)} risk factors across {len(set(risk.country for risk in political_risks))} countries. "
        
        if high_risk_countries:
            countries = list(set(risk.country for risk in high_risk_countries))
            summary += f"High-risk countries include: {', '.join(countries)}. "
        
        if medium_risk_countries:
            countries = list(set(risk.country for risk in medium_risk_countries))
            summary += f"Medium-risk countries include: {', '.join(countries)}. "
        
        summary += "Key risk factors include trade policy changes, labor disputes, and regulatory updates that may impact supply chain operations."
        
        return summary
    
    def _generate_schedule_summary(self, schedule_risks: List[ScheduleRisk]) -> str:
        """Generate executive summary for schedule risks"""
        if not schedule_risks:
            return "No schedule risks identified in current equipment data."
        
        delayed_equipment = [risk for risk in schedule_risks if risk.delay_days > 0]
        high_risk_equipment = [risk for risk in schedule_risks if risk.risk_level >= 4]
        
        total_delay_days = sum(risk.delay_days for risk in delayed_equipment)
        avg_delay = total_delay_days / len(delayed_equipment) if delayed_equipment else 0
        
        summary = f"Schedule analysis identified {len(delayed_equipment)} delayed equipment items out of {len(schedule_risks)} total. "
        summary += f"Average delay: {avg_delay:.1f} days. "
        
        if high_risk_equipment:
            equipment_ids = [risk.equipment_id for risk in high_risk_equipment]
            summary += f"High-risk equipment: {', '.join(equipment_ids)}. "
        
        summary += "Primary risk factors include extended delays, emerging market dependencies, and critical timeline impacts."
        
        return summary
    
    def _generate_combined_summary(self, political_risks: List[PoliticalRisk], 
                                 schedule_risks: List[ScheduleRisk]) -> str:
        """Generate executive summary for combined risks"""
        political_summary = self._generate_political_summary(political_risks)
        schedule_summary = self._generate_schedule_summary(schedule_risks)
        
        return f"Comprehensive Risk Assessment:\n\nPolitical Risks: {political_summary}\n\nSchedule Risks: {schedule_summary}"
    
    def _generate_political_recommendations(self, political_risks: List[PoliticalRisk]) -> List[str]:
        """Generate recommendations for political risks"""
        recommendations = []
        
        if not political_risks:
            return ["Continue monitoring political developments in key supplier countries."]
        
        high_risk_countries = [risk.country for risk in political_risks if risk.likelihood_score >= 4]
        if high_risk_countries:
            recommendations.append(f"Consider diversifying suppliers away from high-risk countries: {', '.join(set(high_risk_countries))}")
        
        trade_risks = [risk for risk in political_risks if "trade" in risk.risk_type.lower()]
        if trade_risks:
            recommendations.append("Monitor trade policy changes and prepare for potential tariff impacts")
        
        labor_risks = [risk for risk in political_risks if "labor" in risk.risk_type.lower()]
        if labor_risks:
            recommendations.append("Develop contingency plans for labor disputes and strikes")
        
        recommendations.append("Establish regular political risk monitoring and early warning systems")
        recommendations.append("Maintain alternative supplier relationships in stable regions")
        
        return recommendations
    
    def _generate_schedule_recommendations(self, schedule_risks: List[ScheduleRisk]) -> List[str]:
        """Generate recommendations for schedule risks"""
        recommendations = []
        
        if not schedule_risks:
            return ["Continue monitoring delivery schedules and maintain supplier relationships."]
        
        high_risk_equipment = [risk for risk in schedule_risks if risk.risk_level >= 4]
        if high_risk_equipment:
            equipment_ids = [risk.equipment_id for risk in high_risk_equipment]
            recommendations.append(f"Expedite delivery for high-risk equipment: {', '.join(equipment_ids)}")
        
        delayed_equipment = [risk for risk in schedule_risks if risk.delay_days > 0]
        if delayed_equipment:
            recommendations.append("Implement daily tracking for all delayed equipment")
            recommendations.append("Establish direct communication channels with delayed suppliers")
        
        recommendations.append("Develop buffer time in project schedules for critical equipment")
        recommendations.append("Create supplier performance scorecards and regular reviews")
        
        return recommendations
    
    def _generate_combined_recommendations(self, political_risks: List[PoliticalRisk], 
                                         schedule_risks: List[ScheduleRisk]) -> List[str]:
        """Generate recommendations for combined risks"""
        political_recs = self._generate_political_recommendations(political_risks)
        schedule_recs = self._generate_schedule_recommendations(schedule_risks)
        
        combined_recs = political_recs + schedule_recs
        combined_recs.append("Integrate political and schedule risk monitoring into unified dashboard")
        combined_recs.append("Develop cross-functional risk management team")
        
        return combined_recs
    
    def _create_world_risk_data(self, political_risks: List[PoliticalRisk]) -> Dict[str, Any]:
        """Create world risk data for visualization"""
        world_data = {}
        
        for risk in political_risks:
            if risk.country not in world_data:
                world_data[risk.country] = {
                    "risk_level": 0,
                    "risk_factors": [],
                    "last_updated": risk.publication_date
                }
            
            world_data[risk.country]["risk_level"] = max(
                world_data[risk.country]["risk_level"], 
                risk.likelihood_score
            )
            world_data[risk.country]["risk_factors"].append(risk.risk_type)
        
        return world_data
    
    def _create_combined_world_risk_data(self, political_risks: List[PoliticalRisk], 
                                       schedule_risks: List[ScheduleRisk]) -> Dict[str, Any]:
        """Create combined world risk data"""
        world_data = self._create_world_risk_data(political_risks)
        
        # Add schedule risks to world data
        for risk in schedule_risks:
            if risk.country not in world_data:
                world_data[risk.country] = {
                    "risk_level": 0,
                    "risk_factors": [],
                    "last_updated": datetime.now().isoformat()
                }
            
            world_data[risk.country]["risk_level"] = max(
                world_data[risk.country]["risk_level"], 
                risk.risk_level
            )
            world_data[risk.country]["risk_factors"].extend(risk.risk_factors)
        
        return world_data
    
    async def generate_downloadable_report(self, report: RiskReport) -> str:
        """Generate downloadable PDF report"""
        filename = f"sentrix_report_{report.report_id}.pdf"
        filepath = os.path.join(self.reports_dir, filename)
        
        doc = SimpleDocTemplate(filepath, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=30,
            alignment=1  # Center alignment
        )
        story.append(Paragraph(report.title, title_style))
        story.append(Spacer(1, 20))
        
        # Report metadata
        meta_data = [
            ['Report ID:', report.report_id],
            ['Session ID:', report.session_id],
            ['Generated:', report.created_at.strftime('%Y-%m-%d %H:%M:%S')],
            ['Type:', report.report_type.title()]
        ]
        
        meta_table = Table(meta_data, colWidths=[100, 200])
        meta_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ]))
        
        story.append(meta_table)
        story.append(Spacer(1, 20))
        
        # Executive Summary
        story.append(Paragraph("Executive Summary", styles['Heading2']))
        story.append(Paragraph(report.executive_summary, styles['Normal']))
        story.append(Spacer(1, 20))
        
        # Political Risks Section
        if report.political_risks:
            story.append(Paragraph("Political Risk Analysis", styles['Heading2']))
            
            # Create political risks table
            political_data = [['Country', 'Risk Type', 'Score', 'Reasoning', 'Source']]
            for risk in report.political_risks:
                political_data.append([
                    risk.country,
                    risk.risk_type,
                    str(risk.likelihood_score),
                    risk.reasoning[:50] + "..." if len(risk.reasoning) > 50 else risk.reasoning,
                    risk.source_title[:30] + "..." if len(risk.source_title) > 30 else risk.source_title
                ])
            
            political_table = Table(political_data, colWidths=[80, 100, 40, 150, 100])
            political_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(political_table)
            story.append(Spacer(1, 20))
        
        # Schedule Risks Section
        if report.schedule_risks:
            story.append(Paragraph("Schedule Risk Analysis", styles['Heading2']))
            
            # Create schedule risks table
            schedule_data = [['Equipment ID', 'Country', 'Delay Days', 'Risk Level', 'Risk Factors']]
            for risk in report.schedule_risks:
                schedule_data.append([
                    risk.equipment_id,
                    risk.country,
                    str(risk.delay_days),
                    str(risk.risk_level),
                    ', '.join(risk.risk_factors[:2])  # Limit to first 2 factors
                ])
            
            schedule_table = Table(schedule_data, colWidths=[80, 80, 60, 60, 120])
            schedule_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(schedule_table)
            story.append(Spacer(1, 20))
        
        # Recommendations
        if report.recommendations:
            story.append(Paragraph("Recommendations", styles['Heading2']))
            for i, rec in enumerate(report.recommendations, 1):
                story.append(Paragraph(f"{i}. {rec}", styles['Normal']))
        
        # Build PDF
        doc.build(story)
        
        return filepath
