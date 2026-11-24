"""Optional PyTorch tests; skipped if the selected interpreter lacks torch."""
import copy
import pytest

torch=pytest.importorskip("torch")
from reliability.assignment51_gru import GRUBinaryClassifier, FEATURES, encode_training_windows, parameter_hash


def fixture():
    rows={i:{**{f:float(i) for f in FEATURES},"timestamp":i*1000,"ue_id":1,"rnti":"a","cellid":1,
              "attack_category":"Benign" if i<3 else "DoS","traffic_type":int(i>=3)} for i in [1,2,3]}
    refs={i:{"cohort":"primary_temporal","source_path":"benign" if i<3 else "attack",
             "provisional_group_id":"b" if i<3 else "a","source_line":i} for i in rows}
    windows=[]
    for ids in [[1,2],[3]]:
        first=ids[0];windows.append({"window_id":str(first),"source_path":refs[first]["source_path"],
            "provisional_group_id":refs[first]["provisional_group_id"],"attack_category":rows[first]["attack_category"],
            "traffic_type":rows[first]["traffic_type"],"expected_report_count":len(ids),
            "report_references":[{"database_rowid":i,"source_line":i} for i in ids],
            "identity":{"ue_id":1,"rnti":"a","cellid":1},"raw_timestamp_first":rows[first]["timestamp"],
            "raw_timestamp_last":rows[ids[-1]]["timestamp"]})
    return rows,windows,refs


def test_scaler_uses_only_real_referenced_training_reports_and_retains_tail():
    rows,windows,refs=fixture();rows[99]={f:1e9 for f in FEATURES}
    x,lengths,y,scaler,ids=encode_training_windows(rows,windows,refs)
    assert x.shape==(2,10,13) and lengths.tolist()==[2,1] and y.tolist()==[0,1]
    assert scaler['mean']==[2.0]*13 and ids==[1,2,3]
    assert x[1,1:].count_nonzero()==0
    assert not set(FEATURES)&{'timestamp','rnti','ue_id','cellid','traffic_type','attack_category','dlBytes','ulBytes'}


def test_packed_model_ignores_padding_and_has_trainable_random_weights(tmp_path):
    torch.manual_seed(42);model=GRUBinaryClassifier();model.eval()
    x=torch.randn(2,10,13);lengths=torch.tensor([2,1]);expected=model(x,lengths)
    changed=x.clone();changed[0,2:]=99999;changed[1,1:]=-99999
    assert torch.equal(expected,model(changed,lengths))
    before=parameter_hash(model)
    optimizer=torch.optim.Adam(model.parameters(),lr=.001)
    loss=torch.nn.BCEWithLogitsLoss()(model(x,lengths),torch.tensor([0.,1.]))
    loss.backward();optimizer.step()
    assert torch.isfinite(loss) and before!=parameter_hash(model)
    p=tmp_path/'state.pt';torch.save(model.state_dict(),p)
    restored=GRUBinaryClassifier();restored.load_state_dict(torch.load(p,weights_only=True));restored.eval()
    assert torch.equal(model(x,lengths),restored(x,lengths))


@pytest.mark.parametrize('problem',['source','clock','label','identity','duplicate','nonfinite'])
def test_invalid_lineage_order_or_values_fail(problem):
    rows,windows,refs=fixture()
    if problem=='source':refs[2]['source_path']='attack'
    if problem=='clock':rows[2]['timestamp']=rows[1]['timestamp']
    if problem=='label':rows[2]['traffic_type']=1
    if problem=='identity':rows[2]['rnti']='other'
    if problem=='duplicate':windows.append(copy.deepcopy(windows[0]))
    if problem=='nonfinite':rows[2][FEATURES[0]]=float('nan')
    with pytest.raises(ValueError):encode_training_windows(rows,windows,refs)
