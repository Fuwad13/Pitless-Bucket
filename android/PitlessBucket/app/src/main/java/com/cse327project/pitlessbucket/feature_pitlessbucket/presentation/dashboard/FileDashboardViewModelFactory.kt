package com.cse327project.pitlessbucket.feature_pitlessbucket.presentation.dashboard

import androidx.lifecycle.ViewModel
import androidx.lifecycle.ViewModelProvider
import com.cse327project.pitlessbucket.feature_pitlessbucket.data.repository.FileRepository


class FileDashboardViewModelFactory(
    private val fileRepository: FileRepository
) : ViewModelProvider.Factory {
    @Suppress("UNCHECKED_CAST")
    override fun <T : ViewModel> create(modelClass: Class<T>): T {
        if (modelClass.isAssignableFrom(FileDashboardViewModel::class.java)) {
            return FileDashboardViewModel(fileRepository) as T
        }
        throw IllegalArgumentException("Unknown ViewModel class")
    }
}