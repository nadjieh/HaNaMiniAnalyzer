{
//=========Macro generated from canvas: c1/c1
//=========  (Fri Jul 21 21:57:55 2017) by ROOT version5.34/19
   TCanvas *c1 = new TCanvas("c1", "c1",13,36,700,500);
   c1->Range(0,0,1,1);
   c1->SetFillColor(0);
   c1->SetBorderMode(0);
   c1->SetBorderSize(2);
   c1->SetFrameBorderMode(0);
   
   TGraphErrors *gre = new TGraphErrors(10);
   gre->SetName("Graph0");
   gre->SetTitle("Graph");
   gre->SetFillColor(1);
   gre->SetPoint(0,20,4.910976);
   gre->SetPointError(0,0,0.08054814);
   gre->SetPoint(1,25,6.236914);
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
   gre->Draw("ap");
   c1->Modified();
   c1->cd();
   c1->SetSelected(c1);
}
