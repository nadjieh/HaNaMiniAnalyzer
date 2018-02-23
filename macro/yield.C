{
//=========Macro generated from canvas: c1/c1
//=========  (Fri Jul 21 21:59:53 2017) by ROOT version5.34/19
   TCanvas *c1 = new TCanvas("c1", "c1",3,26,700,502);
   c1->Range(9.375,3.796077,73.125,10.00218);
   c1->SetFillColor(0);
   c1->SetBorderMode(0);
   c1->SetBorderSize(2);
   c1->SetFrameBorderMode(0);
   c1->SetFrameBorderMode(0);
   
   TGraphErrors *gre = new TGraphErrors(10);
   gre->SetName("Graph0");
   gre->SetTitle("Graph");
   gre->SetFillColor(1);
   gre->SetMarkerStyle(20);
   gre->SetPoint(0,20,4.910976);
   gre->SetPointError(0,0,0.08054814);
   gre->SetPoint(1,24.94612,6.244476);
   gre->SetPointError(1,0,0.09102963);
   gre->SetPoint(2,30,6.155188);
   gre->SetPointError(2,0,0.09106415);
   gre->SetPoint(3,35,6.213163);
   gre->SetPointError(3,0,0.09181226);
   gre->SetPoint(4,40,6.108105);
   gre->SetPointError(4,0,0.09169835);
   gre->SetPoint(5,45,6.017565);
   gre->SetPointError(5,0,0.09068541);
   gre->SetPoint(6,50,6.506307);
   gre->SetPointError(6,0,0.09481374);
   gre->SetPoint(7,55,7.305332);
   gre->SetPointError(7,0,0.09979402);
   gre->SetPoint(8,60,8.444236);
   gre->SetPointError(8,0,0.1068294);
   gre->SetPoint(9,62.5,8.861);
   gre->SetPointError(9,0,0.1068294);
   
   TH1F *Graph_Graph01 = new TH1F("Graph_Graph01","Graph",100,15.75,66.75);
   Graph_Graph01->SetMinimum(4.416688);
   Graph_Graph01->SetMaximum(9.38157);
   Graph_Graph01->SetDirectory(0);
   Graph_Graph01->SetStats(0);

   Int_t ci;      // for color index setting
   TColor *color; // for color definition with alpha
   ci = TColor::GetColor("#000099");
   Graph_Graph01->SetLineColor(ci);
   Graph_Graph01->GetXaxis()->SetLabelFont(42);
   Graph_Graph01->GetXaxis()->SetLabelSize(0.035);
   Graph_Graph01->GetXaxis()->SetTitleSize(0.035);
   Graph_Graph01->GetXaxis()->SetTitleFont(42);
   Graph_Graph01->GetYaxis()->SetLabelFont(42);
   Graph_Graph01->GetYaxis()->SetLabelSize(0.035);
   Graph_Graph01->GetYaxis()->SetTitleSize(0.035);
   Graph_Graph01->GetYaxis()->SetTitleFont(42);
   Graph_Graph01->GetZaxis()->SetLabelFont(42);
   Graph_Graph01->GetZaxis()->SetLabelSize(0.035);
   Graph_Graph01->GetZaxis()->SetTitleSize(0.035);
   Graph_Graph01->GetZaxis()->SetTitleFont(42);
   gre->SetHistogram(Graph_Graph01);
   
   
   TF1 *PrevFitTMP = new TF1("PrevFitTMP","pol7",15.75,66.75);
   PrevFitTMP->SetFillColor(19);
   PrevFitTMP->SetFillStyle(0);
   PrevFitTMP->SetLineColor(2);
   PrevFitTMP->SetLineWidth(2);
   PrevFitTMP->SetChisquare(1.491705);
   PrevFitTMP->SetNDF(2);
   PrevFitTMP->GetXaxis()->SetLabelFont(42);
   PrevFitTMP->GetXaxis()->SetLabelSize(0.035);
   PrevFitTMP->GetXaxis()->SetTitleSize(0.035);
   PrevFitTMP->GetXaxis()->SetTitleFont(42);
   PrevFitTMP->GetYaxis()->SetLabelFont(42);
   PrevFitTMP->GetYaxis()->SetLabelSize(0.035);
   PrevFitTMP->GetYaxis()->SetTitleSize(0.035);
   PrevFitTMP->GetYaxis()->SetTitleFont(42);
   PrevFitTMP->SetParameter(0,-447.2139);
   PrevFitTMP->SetParError(0,202.349);
   PrevFitTMP->SetParLimits(0,0,0);
   PrevFitTMP->SetParameter(1,83.12874);
   PrevFitTMP->SetParError(1,39.41837);
   PrevFitTMP->SetParLimits(1,0,0);
   PrevFitTMP->SetParameter(2,-6.396835);
   PrevFitTMP->SetParError(2,3.199133);
   PrevFitTMP->SetParLimits(2,0,0);
   PrevFitTMP->SetParameter(3,0.2676367);
   PrevFitTMP->SetParError(3,0.1404175);
   PrevFitTMP->SetParLimits(3,0,0);
   PrevFitTMP->SetParameter(4,-0.006570802);
   PrevFitTMP->SetParError(4,0.003605429);
   PrevFitTMP->SetParLimits(4,0,0);
   PrevFitTMP->SetParameter(5,9.461177e-05);
   PrevFitTMP->SetParError(5,5.42411e-05);
   PrevFitTMP->SetParLimits(5,0,0);
   PrevFitTMP->SetParameter(6,-7.396847e-07);
   PrevFitTMP->SetParError(6,4.434028e-07);
   PrevFitTMP->SetParLimits(6,0,0);
   PrevFitTMP->SetParameter(7,2.42384e-09);
   PrevFitTMP->SetParError(7,1.521695e-09);
   PrevFitTMP->SetParLimits(7,0,0);
   gre->GetListOfFunctions()->Add(PrevFitTMP);
   gre->Draw("ap");
   
   TPaveText *pt = new TPaveText(0.4397126,0.9342405,0.5602874,0.995,"blNDC");
   pt->SetName("title");
   pt->SetBorderSize(0);
   pt->SetFillColor(0);
   pt->SetFillStyle(0);
   pt->SetTextFont(42);
   TText *text = pt->AddText("Graph");
   pt->Draw();
   c1->Modified();
   c1->cd();
   c1->SetSelected(c1);
}
