"""Synthetic implementation tests; not the Meridian course known answers."""
import csv, io, unittest
from pathlib import Path
from unittest.mock import patch
import numpy as np
from portfolio import search, estimate, covariance, largest_change

class EngineTests(unittest.TestCase):
 def test_known_grid_reserve_infeasible(self):
  cov=np.eye(2)*.01
  self.assertTrue(np.allclose(search([.1,.1],cov,[True,False],.1,.63)['weights'],[.65,.35]))
  self.assertTrue(np.allclose(search([.1,.1],cov,[False,False],.1,0)['weights'],[.5,.5]))
  self.assertIsNone(search([.01,.02],cov,[True,False],.03,0))
  self.assertIsNone(search([.01,.02],cov,[False,False],0,.03))
 def test_exhaustive_direction(self):
  from itertools import product
  mu=np.array([.02,.05,.08]);cov=np.diag([.01,.04,.09]);result=search(mu,cov,[True,False,False],.055,.03);valid=[]
  for a,b in product(range(21),repeat=2):
   if a+b>20:continue
   w=np.array([a,b,20-a-b])/20
   if w@mu>=.055-1e-12 and w[0]>=.03-1e-12:valid.append(float(w@cov@w))
  self.assertAlmostEqual(result['volatility']**2,min(valid));self.assertEqual(result['grid_mixes'],231)
  self.assertGreaterEqual(result['reserve_weight'],.05-1e-12)
  self.assertGreaterEqual(search(mu,cov,[True,False,False],.065,.03)['volatility'],result['volatility'])
 def test_invalid_covariance(self):
  with self.assertRaises(ValueError):covariance([.1,.1],[[1,2],[2,1]])
  with self.assertRaises(ValueError):search([.1,.1],[[1,2],[0,1]],[True,False])
 @staticmethod
 def prices():
  f=io.StringIO();w=csv.writer(f);w.writerow(['date','TEST_A','TEST_B','TEST_C']);prices=np.ones(3)*100
  for k in range(61):
   if k:prices*=1+np.array([.003+.002*np.sin(k),.004+.003*np.cos(k),.005+.004*np.sin(k*.7)])
   w.writerow([f'{2020+k//12:04d}-{k%12+1:02d}-01',*prices])
  return f.getvalue()
 def test_estimation_bad_data(self):
  text=self.prices();allm=estimate(text);short=estimate(text,True)
  self.assertEqual(allm['observations'],60);self.assertEqual(short['observations'],36)
  px=np.array([[float(v) for v in row[1:]] for row in list(csv.reader(io.StringIO(text)))[1:]]);ret=px[1:]/px[:-1]-1
  self.assertTrue(np.allclose(allm['returns'],ret.mean(axis=0)*12))
  self.assertTrue(np.allclose(short['covariance'],np.cov(ret[-36:],rowvar=False,ddof=1)*12))
  with self.assertRaises(ValueError):estimate(text.replace('2020-02-01','2020-01-01'))
  with self.assertRaises(ValueError):estimate(text.replace('100.0','nan',1))
 def test_ui_missing_inputs(self):
  from streamlit.testing.v1 import AppTest
  at=AppTest.from_file(str(Path(__file__).with_name('app.py')), default_timeout=30).run();at.radio[0].set_value('Meridian training').run();self.assertFalse(at.exception);self.assertTrue(at.error)
  at.radio[0].set_value('My fund prices').run();self.assertFalse(at.exception);self.assertEqual(len(at.file_uploader),1)
 def test_ui_prices_upload_and_window(self):
  from streamlit.testing.v1 import AppTest
  at=AppTest.from_file(str(Path(__file__).with_name('app.py')),default_timeout=30).run()
  at.radio[0].set_value('My fund prices').run()
  at.file_uploader[0].set_value(('synthetic_test_only.csv',self.prices().encode(),'text/csv')).run()
  self.assertFalse(at.exception)
  next(v for v in at.number_input if v.label=='Expected return objective (%)').set_value(4.).run()
  next(v for v in at.number_input if v.label=='Minimum reserve-eligible weight (%)').set_value(0.).run()
  self.assertFalse(at.exception);self.assertEqual(len(at.dataframe[0].value),3)
  self.assertEqual(len(at.get('vega_lite_chart')),2)
  next(v for v in at.checkbox if v.label=='Use last 36 monthly returns').check().run()
  self.assertFalse(at.exception)
  full=estimate(self.prices());short=estimate(self.prices(),True)
  a=search(full['returns'],full['covariance'],[False]*3,.04,0)
  b=search(short['returns'],short['covariance'],[False]*3,.04,0)
  self.assertEqual(at.metric[0].value,f'{largest_change(a,b):.2f} percentage points')
  next(v for v in at.number_input if v.label=='Expected return objective (%)').set_value(99.).run()
  self.assertFalse(at.exception)
  self.assertTrue(any('No mix meets' in v.value for v in at.warning))
 def test_ui_four_sleeve_practice(self):
  from streamlit.testing.v1 import AppTest
  from portfolio import load_proxy
  cfg=load_proxy()
  at=AppTest.from_file(str(Path(__file__).with_name('app.py')),default_timeout=30).run()
  at.radio[0].set_value('Four-sleeve practice').run()
  self.assertFalse(at.exception)
  self.assertTrue(any('Market-proxy practice only' in w.value for w in at.warning))
  expected=search(cfg['returns'],covariance(cfg['volatilities'],cfg['correlations']),cfg['reserve_eligible'])
  self.assertTrue(np.allclose(at.dataframe[0].value['Weight (%)'].tolist(),np.array(expected['weights'])*100))
  field=next(v for v in at.number_input if v.label=='Equity: expected annual return (%)')
  field.set_value(float(cfg['returns'][3]*100-1)).run()
  self.assertFalse(at.exception)
  changed=list(cfg['returns']);changed[3]-=.01
  edited=search(changed,covariance(cfg['volatilities'],cfg['correlations']),cfg['reserve_eligible'])
  self.assertEqual(at.metric[0].value,f'{largest_change(expected,edited):.2f} percentage points')
 def test_ui_shared_engine(self):
  from streamlit.testing.v1 import AppTest
  import portfolio
  cfg={'labels':['Bills','10-year note','IG bonds','Equity'],'returns':[.03,.04,.06,.08],'volatilities':[.01,.05,.09,.16],
       'correlations':np.eye(4).tolist(),'reserve_eligible':[True,True,False,False]}
  with patch.object(portfolio,'load_meridian',return_value=cfg):
   at=AppTest.from_file(str(Path(__file__).with_name('app.py')), default_timeout=30).run();at.radio[0].set_value('Meridian training').run();self.assertFalse(at.exception)
   target=next(x for x in at.number_input if x.label=='Equity: expected annual return (%)');target.set_value(7.).run();self.assertFalse(at.exception)
   original=search(cfg['returns'],covariance(cfg['volatilities'],cfg['correlations']),cfg['reserve_eligible'])
   edited=search([.03,.04,.06,.07],covariance(cfg['volatilities'],cfg['correlations']),cfg['reserve_eligible'])
   self.assertEqual(at.metric[0].value,f'{largest_change(original,edited):.2f} percentage points')
   cfg['correlations'][2][3]=cfg['correlations'][3][2]=.5;at.run();self.assertFalse(at.exception)
   expected=search(cfg['returns'],covariance(cfg['volatilities'],cfg['correlations']),cfg['reserve_eligible'])
   self.assertTrue(np.allclose(at.dataframe[0].value['Weight (%)'].tolist(),np.array(expected['weights'])*100))
if __name__=='__main__':unittest.main(verbosity=2)
