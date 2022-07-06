import pandas as pd
from numpy import unique
from sklearn.cluster import KMeans
from matplotlib import pyplot
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt


class ClusteringController:

    def __init__(self, microtrip_df):
        self.df = microtrip_df
        self.clustered_df = None
        self.clusters = None

    def get_microtrips_number(self):
        """ calculate the number of microtrips"""
        return len(self.df.index)

    def pca(self, n_component, columns):
        """ n_component : number of component of the PCA.
        columns: columns used to execute the PCA
        Transform the data into principal components using PCA.
        Return a dataframe df containing the microtrips described by their new (n_component) component."""
        df = self.df[columns]  # select only columns required for PCA
        df = StandardScaler().fit_transform(df)  # Standardized the features
        pca = PCA(n_components=n_component)
        pca.fit(df)
        pca = pca.transform(df)

        columns = []
        for i in range(len(pca[0])):
            columns.append('Component' + str(i))
            i += 1
        df = pd.DataFrame(pca)
        df.columns = columns
        return df

    def kmeans(self, nb_clusters):
        """Cluster the data using kmeans algorithm. """
        # define the model
        model = KMeans(n_clusters=nb_clusters)
        # fit the model
        model.fit(self.clustered_df)
        # assign a cluster to each example
        yhat = model.predict(self.clustered_df)
        self.clusters = unique(yhat)
        # retrieve unique clusters
        self.df["cluster"] = yhat
        self.clustered_df["cluster"] = yhat

    def select_clustering_columns(self, col, is_pca, n_component=0.80):
        """Select the columns that will be use in the clustering"""
        if is_pca:
            self.clustered_df = self.pca(n_component, col)
        else:
            df = self.df[col]
            df = StandardScaler().fit_transform(df)  # Standardized the features
            df = pd.DataFrame(df)
            df.columns = col
            self.clustered_df = df

    def visualize_cluster_2d(self, xlabel=None, ylabel=None, title="Clustering", show=False, path=None):
        """ Plot the clusters in 2D according do xlabel and ylabel dimensions/columns"""
        if xlabel is None or xlabel not in self.clustered_df.columns :
            xlabel = self.clustered_df.columns[0]

        if ylabel is None or ylabel not in self.clustered_df.columns:
            ylabel = self.clustered_df.columns[1]
        fig = self.clustered_df.plot.scatter(x=xlabel, y=ylabel, c="cluster", colormap='viridis', title=title, legend=False).get_figure()
        if path:
            fig.savefig(path + '.png')
        if show:
            fig.show()

    def visualize_cluster_3d(self, xlabel=None, ylabel=None, zlabel=None):
        """ Plot the clusters in 3D according to xlabel, ylabel, zlabel dimensions/columns"""
        if xlabel is None:
            xlabel = self.clustered_df.columns[0]

        if ylabel is None:
            ylabel = self.clustered_df.columns[1]

        if zlabel is None:
            zlabel = self.clustered_df.columns[2]

        color = ['0.75', 'b', 'g', 'r', 'c', 'm', '0.75', 'y', 'k', '0.45', 'b', 'g', 'r', 'c', 'm', '0.75', 'y',
                 'k']
        fig = plt.figure()
        ax = plt.axes(projection="3d")
        for i in self.clusters:
            x = self.clustered_df[self.clustered_df['cluster'] == i][xlabel]
            y = self.clustered_df[self.clustered_df['cluster'] == i][ylabel]
            z = self.clustered_df[self.clustered_df['cluster'] == i][zlabel]
            ax.scatter3D(x, y, z, c=color[i])
        pyplot.show()
