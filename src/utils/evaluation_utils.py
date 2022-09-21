import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.metrics import (
    plot_confusion_matrix as plot_mdc, 
    plot_roc_curve as plot_roc, 
    classification_report
)

class DummyModel(object):
    
    def __init__(self, y_pred=None, y_prob=None):
        self.y_pred = y_pred
        self.y_prob = y_prob
        self._estimator_type = "classifier"
        self.classes_ = [0, 1]

    def predict(self, X):
        if self.y_pred is None:
            return self.y_pred
        return self.y_pred.values

    def predict_proba(self, X):
        if self.y_prob is None:
            return self.y_prob
        return self.y_prob.values

def plot_confusion_matrix(y_true, y_prob, threshold=0.5, fontsize=26, figsize=(10, 10), cmap='Blues', **kwargs):
    original_fontsize = plt.rcParams['font.size']
    plt.rcParams['font.size'] = fontsize
    y_pred = (y_prob >= threshold).astype(int)
    print(classification_report(y_true, y_pred))
    resp = plot_mdc(
        estimator=DummyModel(y_pred, y_prob),
        X=None, y_true=y_true,
        cmap=cmap, ax=plt.figure(figsize=figsize).gca(), 
        **kwargs
    )
    plt.rcParams['font.size'] = original_fontsize
    return resp

def plot_roc_curve(y_true, y_prob, figsize=(10, 10), **kwargs):
    return plot_roc(
        estimator=DummyModel(y_prob=y_prob),
        X=None, y=y_true,
        ax=plt.figure(figsize=figsize).gca(),
        **kwargs
    )

def calculate_far_frr(y_prob, y_true, n_points=30, normalize=False, threshold=None):
    thr = np.linspace(0, 1, n_points)
    far = []
    frr = []
    for t in thr:
        far_pt = y_prob[y_true == 0] >= t
        frr_pt = y_prob[y_true == 1] <= t
        if normalize:
            far.append(far_pt.mean())
            frr.append(frr_pt.mean())
        else:
            far.append(far_pt.sum())
            frr.append(frr_pt.sum())
    if threshold is None:
        far = np.array(far)
        frr = np.array(frr)
        optm = thr[abs(far - frr).argmin()]
    else:
        optm = threshold
    return {
        'optm': optm,
        'plot': pd.DataFrame(
            index=thr,
            data={
                'far': far,
                'frr': frr,
            },
            dtype=float
        )
    }

def plot_far_frr(figsize=(15,10), grid=True, **kwargs):
    ffdf = calculate_far_frr(**kwargs)
    plt.figure(figsize=figsize)
    ffdf['plot']['far'].plot(ax=plt.gca(), c='red')
    ffdf['plot']['frr'].plot(ax=plt.gca(), c='blue')
    plt.axvline(ffdf['optm'], ls='--', color='#333333', label=f'decisão (threshold >= {ffdf["optm"] * 100:5.2f}%)')
    plt.grid(grid)
    plt.xlim(0, 1)
    plt.ylim(0, ffdf['plot'].max().max())
    plt.xlabel('threshold')
    plt.ylabel('count')
    plt.legend()
    return ffdf

def plot_binary_classifier_histogram(y_true, y_prob, dataset_label=None, threshold=None, **kwargs):
    bins = kwargs.get('bins', 8)
    alpha = kwargs.get('alpha', 0.4)
    linewidth = kwargs.get('linewidth', 0)
    figsize = kwargs.get('figsize', (15, 10))
    fontdict = kwargs.get('fontdict', {'size': 12})

    plt.figure(figsize=figsize)
    sns.histplot(
        y_prob[y_true == 0], color='red', label='y==0',
        bins=bins, alpha=alpha, linewidth=linewidth
    )
    sns.histplot(
        y_prob[y_true == 1], color='blue', label='y==1',
        bins=bins, alpha=alpha, linewidth=linewidth
    )
    if threshold is not None:
        plt.axvline(0.5, ls='--', color='#333333', label=f'decisão (threshold >= {threshold * 100:5.2f}%)')
    plt.xlabel('Probabilidade', fontdict={'size': 12})
    plt.ylabel('Contagem', fontdict={'size': 12})
    if dataset_label is not None:
        dataset_label = f' - {dataset_label}'
    plt.title(f'Estimativas {dataset_label}', fontdict={'size': 12})
    plt.grid(True)
    plt.legend()
    return plt

def prepare_df(X_df, y_df, model):
  X = X_df
  y_true = y_df.values.flatten()
  y = pd.DataFrame(
      dict(
          y_true=y_true,
          y_pred=model.predict(X),
          y_prob=model.predict_proba(X)[:, 1]
      ),
      index=X.index    
  )
  return y, y_true, X

def plot_all(X_df, y_df, model):
  y, y_true, X = prepare_df(X_df, y_df, model)
  f, axes = plt.subplots(2, 2, figsize=(20, 10))
  f.subplots_adjust(hspace=.3, wspace=.25)
  plot_roc(
          estimator=DummyModel(y_prob=y.y_prob),
          X=None, y=y_true,
          ax=axes[0][0],
          name=''
        )

  # original_fontsize = plt.rcParams['font.size']
  # plt.rcParams['font.size'] = fontsize
  threshold=0.5
  y_pred = (y.y_prob >= threshold).astype(int)
  print(classification_report(y_true, y_pred))
  resp = plot_mdc(
      estimator=DummyModel(y_pred, y.y_prob),
      X=None, y_true=y_true,
      cmap='Blues', ax=axes[1][0], 
      values_format='d'
  )


  ffdf = calculate_far_frr(y_prob=y.y_prob, y_true=y.y_true)
  ffdf['plot']['far'].plot(ax=axes[0][1], c='red')
  ffdf['plot']['frr'].plot(ax=axes[0][1], c='blue')
  axes[0][1].plot(ax=axes[0][1])
  axes[0][1].axvline(ffdf['optm'], ls='--', color='#333333', label=f'decisão (threshold >= {ffdf["optm"] * 100:5.2f}%)')
  axes[0][1].grid(True)
  plt.xlim(0, 1)
  plt.ylim(0, ffdf['plot'].max().max())
  plt.xlabel('threshold')
  plt.ylabel('count')
  axes[0][1].legend()
  # plt.rcParams['font.size'] = original_fontsize

  bins = 8
  alpha = 0.4
  dataset_label='Massa de Teste'
  sns.histplot(
      y.y_prob[y_true == 0], color='red', label='y==0',
      bins=bins, alpha=alpha, cbar_ax=axes[1][1]
  )
  sns.histplot(
      y.y_prob[y_true == 1], color='blue', label='y==1',
      bins=bins, alpha=alpha, cbar_ax=axes[1][1]
  )
  plt.xlabel('Probabilidade', fontdict={'size': 12})
  plt.ylabel('Contagem', fontdict={'size': 12})
  if dataset_label is not None:
      dataset_label = f' - {dataset_label}'
  plt.title(f'Estimativas {dataset_label}', fontdict={'size': 12})
  axes[1][1].grid(True)
  plt.legend()
  plt.savefig('../frontend/pages/evaluation.png')
