from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

import sys
import pytest

from male import random_seed
from male.callbacks import Display
from male.models.distribution import GMM
from male.models.distribution import Gaussian1D
from male.models.deep_learning.generative import GAN2D


@pytest.mark.skipif('tensorflow' not in sys.modules, reason="requires tensorflow library")
def test_gan2d_gmm2d(block_figure_on_end=False):
    loss_display = Display(layout=(2, 1),
                           dpi='auto',
                           title='Loss',
                           block_on_end=block_figure_on_end,
                           monitor=[{'metrics': ['d_loss', 'g_loss'],
                                     'type': 'line',
                                     'labels': ["discriminator loss", "generator loss"],
                                     'title': "Losses",
                                     'xlabel': "epoch",
                                     'ylabel': "loss",
                                     },
                                    {'metrics': ['loglik'],
                                     'type': 'line',
                                     'labels': ["Log-likelihood"],
                                     'title': "Evaluation",
                                     'xlabel': "epoch",
                                     'ylabel': "loglik",
                                     },
                                    ])
    scatter_display = Display(layout=(1, 1),
                              dpi='auto',
                              freq=10,
                              title='Scatter',
                              block_on_end=block_figure_on_end,
                              monitor=[{'metrics': ['scatter'],
                                        'type': 'scatter',
                                        'title': "Data scatter generated by GAN2D",
                                        'num_samples': 1000,
                                        'xlim': (-4, 4),
                                        'ylim': (-4, 4),
                                        },
                                       ])

    num_mixtures = 8
    radius = 2.0
    std = 0.02
    import numpy as np
    thetas = np.linspace(0, 2 * np.pi, num_mixtures + 1)[:num_mixtures]
    xs, ys = radius * np.sin(thetas), radius * np.cos(thetas)

    model = GAN2D(
        data=GMM(mix_coeffs=[1 / num_mixtures] * num_mixtures,
                 mean=list(zip(xs, ys)),
                 cov=[[std, std]] * num_mixtures),
        num_z=10,  # set to 256 for a full run
        generator=Gaussian1D(mu=0.0, sigma=1.0),
        num_epochs=4,  # set to 25000 for a full run
        hidden_size=16,  # set to 128 for a full run
        batch_size=16,  # set to 128 for a full run
        loglik_freq=1,
        generator_learning_rate=0.0001,
        discriminator_learning_rate=0.0001,
        metrics=['d_loss', 'g_loss', 'loglik'],
        callbacks=[loss_display, scatter_display],
        random_state=random_seed(),
        verbose=1)
    model.fit()


if __name__ == '__main__':
    pytest.main([__file__])
    # test_gan2d_gmm2d(block_figure_on_end=True)